
/****************************************************************************
 * smoke_tb.sv
 ****************************************************************************/

  
/**
 * Module: smoke_tb
 * 
 * TODO: Add module documentation
 */
module smoke_tb(input clock);
	
`ifdef HAVE_HDL_CLOCKGEN
	reg clock_r;
	
	initial begin
		forever begin
			#10ns;
			clock_r <= ~clock_r;
		end
	end
	
	assign clock = clock_r;
`endif


endmodule


