"""Controles analíticos independentes. Não constituem validação do Eberick."""
import math
import unittest

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

from grelha import element, consistent, condense
from verificar import capacity, CENTRE, AS_FACE, FCD, FYD


class BarraAnalitica(unittest.TestCase):
    def setUp(self):
        self.E, self.G, self.A = 3000., 1200., 600.
        self.L, self.I2, self.I3 = 88., 20000., 45000.
        self.section = dict(Shape='General', Area='600', AMod='1',
                            I22='20000', I33='45000', I2Mod='1', I3Mod='1',
                            TorsConst='15000', JMod='1')
        self.mat = dict(E1='3000', G12='1200')
        self.k, self.rot, _ = element([0., 0., 0.], [88., 0., 0.],
                                      self.section, self.mat, 0)

    def test_cantilever_ponta_dois_planos(self):
        for translation, rotation, inertia, sign in ((7,11,self.I3,1),(8,10,self.I2,-1)):
            with self.subTest(translation=translation):
                force = np.zeros(12)
                force[translation] = 11.
                u = np.zeros(12)
                u[6:] = np.linalg.solve(self.k[6:,6:], force[6:])
                self.assertAlmostEqual(u[translation], 11*self.L**3/(3*self.E*inertia), 10)
                self.assertAlmostEqual(u[rotation], sign*11*self.L**2/(2*self.E*inertia), 10)
                reactions = self.k @ u - force
                self.assertAlmostEqual(reactions[translation-6], -11, 8)
                self.assertAlmostEqual(reactions[rotation-6], -sign*11*self.L, 8)

    def test_alongamento_e_torcao(self):
        self.assertAlmostEqual(self.k[0,0], self.E*self.A/self.L)
        self.assertAlmostEqual(self.k[3,3], self.G*15000/self.L)

    def test_seis_movimentos_rigidos_e_simetria(self):
        np.testing.assert_allclose(self.k, self.k.T)
        # Local: primeira barra na direção 1, ponta J a L do nó I.
        for index in range(6):
            d = np.zeros(12)
            d[index] = d[index+6] = 1
            if index == 4:
                d[8] = -self.L
            if index == 5:
                d[7] = self.L
            np.testing.assert_allclose(self.k @ d, 0, atol=1e-7)

    def test_rotacao_arbitraria_preserva_energia(self):
        k, rot, _ = element([3.,5.,7.],[11.,20.,31.], self.section,self.mat,23.)
        np.testing.assert_allclose(rot @ rot.T, np.eye(12), atol=1e-14)
        u = np.arange(12, dtype=float)/17
        self.assertAlmostEqual(u @ (rot.T @ k @ rot) @ u, (rot @ u) @ k @ (rot @ u), 7)

    def test_eixos_horizontal_e_vertical(self):
        np.testing.assert_allclose(self.rot[:3,:3], [[1,0,0],[0,0,1],[0,-1,0]])
        _, rot, _ = element([0.,0.,0.],[0.,0.,self.L],self.section,self.mat,0.)
        np.testing.assert_allclose(rot[:3,:3], [[0,0,1],[1,0,0],[0,1,0]])

    def test_carga_uniforme_engastada_e_biapoiada(self):
        for direction, rotation, sign in ((1,5,1),(2,4,-1)):
            q = np.zeros(3)
            q[direction] = 2.5
            f = consistent(q,self.L)
            self.assertAlmostEqual(f[direction], 2.5*self.L/2)
            self.assertAlmostEqual(f[rotation], sign*2.5*self.L**2/12)
            original_k = self.k.copy()
            original_f = f.copy()
            k2, f2 = condense(self.k, f[:,None], [rotation,rotation+6])
            self.assertAlmostEqual(f2[direction,0], 2.5*self.L/2)
            np.testing.assert_allclose(f2[[rotation,rotation+6]],0)
            np.testing.assert_allclose(k2[[rotation,rotation+6]],0)
            np.testing.assert_array_equal(original_k,self.k)
            np.testing.assert_array_equal(original_f,f)

    def test_deformacao_cisalhante_cantilever(self):
        k,_,_=element([0.,0.,0.],[88.,0.,0.],self.section,self.mat,0.,5/6)
        f=np.zeros(6)
        f[1]=11.
        d=np.linalg.solve(k[6:,6:],f)
        expected=11*self.L**3/(3*self.E*self.I3)+11*self.L/((5/6)*self.G*self.A)
        self.assertAlmostEqual(d[1],expected,10)


class SecaoConcreto(unittest.TestCase):
    @staticmethod
    def independent(h,b,n):
        # Quadratura adaptativa em toda a altura, independente da divisão de Gauss.
        d=h-CENTRE
        def response(x):
            curvature=min(.0035/x,.010/(d-x))
            def concrete(y):
                strain=curvature*(x-y)
                if strain<=0:
                    return 0.
                return .85*FCD*(1-(1-min(strain,.002)/.002)**2)
            breaks=sorted(set([0.,max(0.,x-.002/curvature),x,h]))
            normal=quad(lambda y:b*concrete(y),0,h,points=breaks)[0]
            moment=quad(lambda y:b*concrete(y)*(h/2-y),0,h,points=breaks)[0]
            for y in (CENTRE,d):
                stress=max(-FYD,min(FYD,210000*curvature*(x-y)))
                force=AS_FACE*(stress-concrete(y))
                normal+=force
                moment+=force*(h/2-y)
            return normal/1000,moment/1e6
        x=brentq(lambda x:response(x)[0]-n,.001,d-.00001)
        return response(x)[1],x/d

    def test_quadratura_independente_e_ductilidade(self):
        for h,b in ((300,200),(200,300)):
            for n in (-.5,0,5,18):
                with self.subTest(h=h,n=n):
                    independent,xd=self.independent(h,b,n)
                    self.assertAlmostEqual(capacity(h,b,n),independent,8)
                    self.assertLess(xd,.45)

    def test_minimos_nos_extremos_intervalo_estudado(self):
        for h,b in ((300,200),(200,300)):
            boundary=min(capacity(h,b,n) for n in (-.5,18))
            for n in np.linspace(-.5,18,50):
                self.assertGreaterEqual(capacity(h,b,n)+1e-10,boundary)

    def test_ordem_de_grandeza_flexao(self):
        # Uma única face de aço escoando fornece uma referência de ordem de grandeza.
        for h,b in ((300,200),(200,300)):
            reference=AS_FACE*FYD*.9*(h-CENTRE)/1e6
            self.assertGreater(capacity(h,b,0),reference*.85)
            self.assertLess(capacity(h,b,0),reference*1.2)


if __name__=='__main__':
    unittest.main()
