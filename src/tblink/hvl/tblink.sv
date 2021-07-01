/****************************************************************************
 * tblink.sv
 * 
 * SystemVerilog integration shim for TBLink
 ****************************************************************************/
  
`ifdef VERILATOR
/**
 * Package: tblink
 * 
 * Implements TbLink integration for SV-DPI simulators
 * without support for time-consuming tasks
 */
package tblink;
	
	/****************************************************************
	 * Python API wrappers
	 ****************************************************************/

	/**
	 * Function: register_scope
	 * 
	 * Registers a DPI scope handle with the library and associates
	 * a key with it
	 * 
	 * Parameters:
	 * - string key 
	 * 
	 * Returns:
	 * - Dummy value (1) to enable static registration
	 */
	function int register_scope(string key);
		if (_tblink_dpi_register_scope(key) == 0) begin
			$display("Error: failed to register scope %s", key);
			$finish;
		end
		return 1;
	endfunction
	import "DPI-C" function int _tblink_dpi_register_scope(string key);
	

	import "DPI-C" context function int _tblink_dpi_init(
			int have_blocking_tasks
	);
	function int _init_tblink();
		int ret;
		
		ret = _tblink_dpi_init(
			`ifdef VERILATOR
				0 // Does not support blocking task calls
			`else
				1 // Other simulators do
			`endif
		);
		
		if (ret != 1) begin
			$display("Error: Failed to initialize PyTblink backend");
			$finish();
			end
		
		return ret;
	endfunction
	
	int _init = _init_tblink();
	
	// For simplicity, we still provide the export
	// even though Verilator uses a different mechanism
	function int _tblink_register_timed_callback(
		longint unsigned		delta
		);
		$display("Error: tblink_register_timed_callback called from Verilator");
		$finish;
	endfunction
	export "DPI-C" function _tblink_register_timed_callback;

endpackage

`else /* !VERILATOR */

/**
 * Module: tblink
 * 
 * Hosts thread-creation site for tblink
 */
module tblink();
	// Requests for new threads are queued here
	typedef class timed_cb;
	mailbox #(timed_cb)   cb_q = new();

	// For simulators with support for time-consuming
	// DPI tasks, register the tblink interface here
	import "DPI-C" context function int _tblink_dpi_init(
			int have_blocking_tasks
	);
	
	function int _init_tblink();
		if (_tblink_dpi_init(1) != 1) begin;
			$display("Error: Failed to initialize PyTblink backend");
			$finish();
		end
		
		return 1;
	endfunction
	
	int _init = _init_tblink();
	
	/****************************************************************
	 * timed_cb
	 * Helper class to support timed callbacks
	 ****************************************************************/
	class timed_cb;
		static timed_cb         m_active_cb[$];
		int unsigned			m_id;
		longint unsigned		m_delta;
		bit						m_valid = 1;
		
		function new(
			int unsigned		id,
			longint unsigned 	delta);
			m_id = id;
			m_delta = delta;
			m_active_cb[id] = this;
		endfunction
		
		function void start();
			fork
				begin
					run();
				end
			join_none
		endfunction
		
		static function int alloc_id();
			int ret = -1;
			for (int i=0; i<m_active_cb.size(); i++) begin
				if (m_active_cb[i] == null) begin
					ret = i;
					break;
				end
			end
			
			if (ret == -1) begin
				ret = m_active_cb.size();
				m_active_cb.push_back(null);
			end
			
			return ret;
		endfunction
		
		task run();
			#(m_delta*1ns);
			if (m_valid) begin
				_tblink_timed_callback(m_id);
			end
			// Remove ourselves from the active callback list
			m_active_cb[m_id] = null;
		endtask
	endclass
	
	/****************************************************************
	 * _tblink_timed_callback()
	 * 
	 * Notify the backend of a DPI callback. 
	 ****************************************************************/
	import "DPI-C" context function void _tblink_timed_callback(int id);

	/****************************************************************
	 * _tblink_register_timed_callback()
	 * 
	 * Export function used to register a timed callback. This is 
	 * used for most simulators except for Verilator, which does 
	 * not support time-consuming functions.
	 ****************************************************************/
	function int _tblink_register_timed_callback(
		longint unsigned		delta
		);
		automatic int unsigned id = timed_cb::alloc_id();
		automatic timed_cb cb = new(id, delta);
		
		void'(cb_q.try_put(cb));
		
		return id;
	endfunction
	export "DPI-C" function _tblink_register_timed_callback;
		
	/**
	 * SV threads must be started by the simulator. 
	 * This process accepts requests from Python and
	 * forks new threads in response
	 */
	initial begin
		forever begin
			automatic timed_cb cb;
			cb_q.get(cb);
			
			fork
				cb.run();
			join_none
		end
	end
endmodule
`endif /* !VERILATOR */

