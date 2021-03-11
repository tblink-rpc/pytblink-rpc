/****************************************************************************
 * tblink_pkg.sv
 * 
 * SystemVerilog integration shim for TBLink
 ****************************************************************************/
  
/**
 * Package: tblink_pkg
 * 
 * TODO: Add package documentation
 */
package tblink_pkg;
	
	/****************************************************************
	 * Initialization code
	 ****************************************************************/
	import "DPI-C" context function int _tblink_dpi_init(
			int have_blocking_tasks
	);

	import "DPI-C" function chandle _tblink_pylist_new(int unsigned sz);
	
	function int _init_tblink();
		int ret;
		chandle l;
		
		ret = _tblink_dpi_init(
`ifdef VERILATOR
			0 // Does not support blocking task calls
`else
			1 // Other simulators do
`endif
			);
		
//		l = _tblink_pylist_new(10);
//		$display("l=%p", l);
		
		if (ret != 1) begin
			$display("Error: Failed to initialize PyTblink backend");
			$finish();
		end
		
		return ret;
	endfunction
		
	int _init = _init_tblink();

`ifndef VERILATOR
	/****************************************************************
	 * timed_cb
	 * Helper class to support timed callbacks
	 ****************************************************************/
	class timed_cb;
		int unsigned			m_id;
		longint unsigned		m_delta;
		bit						m_valid = 1;
		
		function new(
			int unsigned		id,
			longint unsigned 	delta);
			m_id = id;
			m_delta = delta;
		endfunction
		
		task run();
			#(m_delta*1ps);
//			prv_active_cb.delete()
			if (m_valid) begin
				_tblink_timed_callback(m_id);
			end
		endtask
	endclass
	
	int unsigned					prv_cb_id;
	timed_cb						prv_active_cb;
	
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
		int unsigned id = prv_cb_id;
		timed_cb cb = new(id, delta);
		
		prv_cb_id++;
		
		fork
			cb.run();
		join_none

		return id;
	endfunction
	export "DPI-C" function _tblink_register_timed_callback;

	/****************************************************************
	 * _tblink_timed_callback()
	 * 
	 * Notify the backend of a DPI callback. 
	 ****************************************************************/
	import "DPI-C" function void _tblink_timed_callback(int id);
	
`else /* Verilator */
	// For simplicity, we still provided the export
	// even though Verilator uses a different mechanism
	function int _tblink_register_timed_callback(
		longint unsigned		delta
		);
		$display("Error: tblink_register_timed_callback called from Verilator");
		$finish;
	endfunction
	export "DPI-C" function _tblink_register_timed_callback;
	
`endif /* VERILATOR */

endpackage


