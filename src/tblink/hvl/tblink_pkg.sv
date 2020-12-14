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
	int _init = _tblink_dpi_init(
`ifdef VERILATOR
			0 // Does not support blocking task calls
`else
			1 // Other simulators do
`endif
			);
	

`ifndef VERILATOR
	/****************************************************************
	 * timed_cb
	 * Helper class to support timed callbacks
	 ****************************************************************/
	class timed_cb;
		int unsigned				m_id;
		longint unsigned			m_delta;
		bit							m_valid = 1;
		
		function new(
			int unsigned		id,
			longint unsigned 	delta);
			m_id = id;
			m_delta = delta;
		endfunction
		
		task run();
			# (m_delta*1ps);
			prv_active_cb.delete(
			if (m_valid) begin
				_tblink_timed_callback();
			end
		endtask
	endclass
	
	int unsigned					prv_cb_id;
	timed_cb						prb_active_cb;
	
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
		prv_cb_id++;
		timed_cb cb = new(id, delta);
		
		fork
			cb.run();
		join_none

		return id;
	endfunction
	export "DPI-C" function _tblink_register_timed_callback;

	/****************************************************************
	 * _tblink_timed_callback()
	 * 
	 * Notify the backend of a DPI callback. This is a task, since
	 * calling this could result in consuming time.
	 ****************************************************************/
	import "DPI-C" task _tblink_timed_callback();
	
`endif /* VERILATOR */

endpackage


