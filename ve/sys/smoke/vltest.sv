
package cls_pkg;

	class pyval_c;
	endclass

	class param_c;
	endclass

	class pyargs_c;
	endclass

	class list_c;
		pyval_c		elems[$];
		
		function new();
		endfunction

		function void add_i(int v);
			pyval_c pv = new();
			$display("i(%0d)", v);
			elems.push_back(pv);
		endfunction

		function void add_s(string v);
			pyval_c pv = new();
			$display("s(%0s)", v);
			elems.push_back(pv);
		endfunction

		function list_c i(int v);
`ifndef VERILATOR
			add_i(v);
			return this;
`else
			$display("Error: Verilator doesn't support 'this'");
			$finish();
			return null;
`endif
		endfunction

		function list_c s(string v);
`ifndef VERILATOR
			add_s(v);
			return this;
`else
			$display("Error: Verilator doesn't support 'this'");
			$finish();
			return null;
`endif
		endfunction
	endclass

	function automatic list_c list();
		list_c ret = new();
		return ret;
	endfunction

endpackage

module top(input clock);
import cls_pkg::*;

initial begin
	$display("Hello");
`ifndef VERILATOR
	begin
	automatic list_c l = list().i(5).s("boo").i(20);
	end
`else
	begin
	automatic list_c l = list();
	l.add_i(5);
	l.add_s("boo");
	l.add_i("20");
	end
`endif

end

endmodule

