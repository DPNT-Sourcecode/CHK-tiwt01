from solutions.CHK import checkout_solution

class TestChk():
    def test_invalid(self):
        assert checkout_solution.checkout('ABCxAC') == -1
    
    def test_parse(self):
        assert checkout_solution.parse_skus('ABCAC') == {'A':2, 'B': 1, 'C': 2}
    
    def test_chk(self):
        assert checkout_solution.checkout('ABCDE') == 155

    def test_multiples(self):
        assert checkout_solution.checkout('ABCACD') == 185

    def test_special_a(self):
        assert checkout_solution.checkout('ABCACDA') == 215

    def test_special_a5(self):
        assert checkout_solution.checkout('ABACACADA') == 285

    def test_special_a7(self):
        assert checkout_solution.checkout('ABACACADAAA') == 385

    def test_special_b(self):
        assert checkout_solution.checkout('ABCACDB') == 200

    def test_special_eeb(self):
        assert checkout_solution.checkout('EEB') == 80

    def test_special_eeeb(self):
        assert checkout_solution.checkout('EEEB') == 120

    def test_special_eeeebb(self):
        assert checkout_solution.checkout('EEEEBB') == 160

    def test_special_multi_basic(self):
        assert checkout_solution.checkout('STX') == 45
        
    def test_special_multi_mixed(self):
        assert checkout_solution.checkout('STXAB') == 125
        
    def test_special_multi_multi(self):
        assert checkout_solution.checkout('STXABYZS') == 170
