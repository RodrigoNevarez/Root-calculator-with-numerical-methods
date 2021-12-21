# Name: python root_calculator.py
# Author: Rodrigo Nevarez Escobar
# Date: 24 / 09 / 2020
# Description: A function's root calculator.

import math
from os import system

class RootCalculator:
	'''Clase principal para manejar recursos de la calculadora'''

	def __init__(self):
		'''Inicializar recursos de la calculadora.'''
		self.calculator_active = True
		self.interval = {'left': 0.2, 'right': 1.5}
		self.function = 'f(x) = x^3.3 - 79'
		self.trunc_error = 0.001
		self.iterations = 3
		self.mode = 'iteraciones'
		self.method = 'falsa_posición'

	def run_calculator(self):
		'''Proceso principal de la calculadora'''
		while True:
			if not self.calculator_active:
				break
			command = self._show_main_menu()
			if command == '!aproximar_raíz':
				self._aproximate_root()
			elif command == '!cambiar_intervalo':
				self._change_interval()
			elif command == '!cambiar_método':
				self._change_method()
			elif command == '!cambiar_modo':
				self._change_mode()
			elif command == '!créditos':
				self._show_credits()
			elif command == '!salir':
				input("¡Gracias por usar la calculadora!"
					"\npresione cualquier tecla para continuar...")
				self.calculator_active = False
			else:
				print('Comando no identificado, por favor intente denuevo.')
				input('Presione cualquier botón para continuar...')
				system('cls')

	def _show_main_menu(self):
		'''
		Muestra el menú principal
		Regresa un comando
		'''
		print(f'Función: {self.function}')
		print(f"Intervalo: ({self.interval['left']} , {self.interval['right']})")
		print(f'Método: {self.method}')
		print(f'Modo: {self.mode}')
		if self.mode == 'iteraciones':
			print(f'Iteraciones: {self.iterations}')
		elif self.mode == 'error_truncamiento':
			print(f'Error de truncamiento: {self.trunc_error}')
		print('\nEl siguiente algoritmo aproxima la raiz de '
			f'<<{self.function}>> usando <<{self.method}>>.')
		print('\n!aproximar_raíz'
			'\n!cambiar_intervalo'
			'\n!cambiar_método'
			'\n!cambiar_modo'
			'\n!créditos'
			'\n!salir\n')
		command = input('Inserta un comando: ')
		print('-----------------------------------------------------------------')
		return command

	def _evaluate_function(self, x):
		"""Evaluar un número en la función."""
		x = (x ** 3) + x - 2
		return x

	def _aproximate_root(self):
		'''Aproxima la raiz de la función'''
		original_left = self.interval['left']
		original_right = self.interval['right']

		root_found = self._check_interval()
		if not root_found:
			if self.mode == 'iteraciones':
				for i in range(self.iterations):
					if self.method == 'bisección':
						root = self._bisection(i)
					elif self.method == 'falsa_posición':
						root = self._false_position(i)

					if self._evaluate_function(root) == 0:
						root_found = True
						break

			elif self.mode == 'error_truncamiento':
				k = self._determine_k()
				for i in range(k+1):
					if self.method == 'bisección':
						root = self._bisection(i)
					elif self.method == 'falsa_posición':
						root = self._false_position(i)

					if self._evaluate_function(root) == 0:
						root_found = True
						break
			if root_found:
				print(f"\nla raíz de <<{self.function}>> es igual a <<({root}, 0)>>.")
			else:
				print(f"\nla raíz de <<{self.function}>> es aproximada a <<({root}, 0)>>.")
		
		input('Presione cualquier botón para continuar...')
		self._reset_interval(original_left, original_right)
		system('cls')

	def _check_interval(self, root_found = False):
		'''
		Revisar si la raíz no se encuentra en uno o ambos extremos del intervalo.
		Regresar True o False.
		'''
		if self._evaluate_function(self.interval['left']) == 0:
			root = self.interval['left']
			print(f"\nla raíz de <<{self.function}>> es igual a <<({root}, 0)>>.\n")
			root_found = True
		if self._evaluate_function(self.interval['right']) == 0:
			root = self.interval['right']
			print(f"la raíz de <<{self.function}>> es igual a <<({root}, 0)>>.\n")
			root_found = True
		return root_found

	def _determine_k(self):
		'''
		Determinar el número de subindices.
		Regresar número de subindices.
		'''
		numerator = math.log((self.interval['right'] - self.interval['left']) / self.trunc_error)
		denominator = math.log(2)
		k = (numerator / denominator) - 1
		k = math.ceil(k)
		return k

	def _bisection(self, i):
		'''
		Aproximar la raiz por bisección.
		Regresa la aproximación de la raíz.
		'''
		midpoint = (self.interval['left'] + self.interval['right']) / 2
		f_midpoint = self._evaluate_function(midpoint)
		
		self._print_line(n=i, xn=midpoint, f_xn=f_midpoint)
		
		if f_midpoint == 0:
			return midpoint
		else:
			self._determine_next_interval(midpoint, f_midpoint)
			return midpoint

	def _false_position(self, i):
		'''
		Aproximar la raiz por falsa posición.
		Regresa la aproximación de la raíz.
		'''
		secant_intercetion = self._get_secant_intersection()
		f_secant_intercetion = self._evaluate_function(secant_intercetion)

		self._print_line(n=i, xn=secant_intercetion, f_xn=f_secant_intercetion)

		if f_secant_intercetion == 0:
			return secant_intercetion
		else:
			self._determine_next_interval(secant_intercetion, f_secant_intercetion)
			return secant_intercetion

	def _get_secant_intersection(self):
		'''
		Conseguir la intersección con x de la secante que une a y b.
		Regresar raíz de la secante.
		'''
		f_a = self._evaluate_function(self.interval['left'])
		f_b = self._evaluate_function(self.interval['right'])
		numerator = self.interval['right'] - self.interval['left']
		denominator = f_b - f_a
		c = self.interval['right'] - (f_b * (numerator / denominator))
		return c

	def _determine_next_interval(self, c, f_c):
		'''Determinar el siguiente intervalo.'''
		f_a = self._evaluate_function(self.interval['left'])
		f_b = self._evaluate_function(self.interval['right'])

		if self._sign(f_c) == self._sign(f_a):
			self.interval['left'] = c
		elif self._sign(f_c) == self._sign(f_b):
			self.interval['right'] = c

	def _sign(self, n):
		'''
		Determinar el signo de un número.
		Regresar True si positivo.
		Regresar False si negativo.

		'''
		if n >= 0:
			return True
		return False

	def _print_line(self, n, xn, f_xn):
		'''Imprime una linea de la tabla de bisección.'''	
		# Imprime encabezado de tabla
		f_an = self._evaluate_function(self.interval['left'])
		f_bn = self._evaluate_function(self.interval['right'])

		if n == 0:	
			print("\n|  n  |  an  |  bn  |  xn  |  f(an)  |  f(bn)  |  f(xn)  |\n")
		print(f"| {n} | {self.interval['left']} | {self.interval['right']} | {xn} | {f_an} | {f_bn} | {f_xn} |\n")

	def _reset_interval(self, a, b):
		'''Restaurar los valores originales del intervalo.'''
		self.interval['left'] = a
		self.interval['right'] = b

	def _change_mode(self):
		'''Cambia el modo en el que cálcula la raíz.'''
		print('Escriba el comando del modo que desea:')
		print('!iteraciones'
			'\n!error_truncamiento')
		while True:
			command = input('Inserta un comando: ')
			if command == '!iteraciones':
				self.iterations = self._float_input('Número de iteraciones: ', True)
				self.mode = 'iteraciones'
				system('cls')
				return
			elif command == '!error_truncamiento':
				self.trunc_error = self._float_input('Error de truncamiento: ')
				self.mode = 'error_truncamiento'
				system('cls')
				return
			else:
				print('Comando no identificado, por favor intente denuevo.')

	def _change_method(self):
		'''Cambia el método en el que cálcula la raíz.'''
		print('Escriba el comando del modo que desea:')
		print('!bisección'
			'\n!falsa_posición')
		while True:
			command = input('Inserta un comando: ')
			if command == '!bisección':
				self.method = 'bisección'
				system('cls')
				return
			elif command == '!falsa_posición':
				self.method = 'falsa_posición'
				system('cls')
				return
			else:
				print('Comando no identificado, por favor intente denuevo.')

	def _change_interval(self):
		'''Capturar el intervalo.'''
		root_not_found = True
		while root_not_found:

			lvalue = self._float_input("Extremo izquierdo: ")
			rvalue = self._float_input("Extremo derecho: ")
			has_root = self._check_root(lvalue, rvalue)
			is_correct = self._check_position(lvalue, rvalue)

			if has_root and is_correct:
				self.interval['left'] = lvalue
				self.interval['right'] = rvalue
				root_not_found = False
			
			elif not is_correct:
				print("(!) Lo sentimos,"
					" su intervalo no es valido. Intente denuevo.\n")

			elif not has_root:
				print("(!) Lo sentimos,"
					" al parecer su intervalo no tiene raíz. Intente denuevo.\n")
		system('cls')

	def _float_input(self, message, integer = False):
		'''
		Captura un número real, atrapa error de valor
		Regresa el número capturado
		'''
		while True:
			try:
				if integer:
					n = int(input(message))
				else:
					n = float(input(message))
			except ValueError:
				print(f"(!) Entrada no es un número, intente denuevo.\n")
			else:
				return n 

	def _check_root(self, lvalue, rvalue):
		"""
		Revisar si existe una raíz en el intervalo 
		Regresa True o False
		"""
		f_a = self._evaluate_function(lvalue)
		f_b = self._evaluate_function(rvalue)
		c = f_a * f_b
		if c <= 0:
			return True
		else:
			return False

	def _check_position(self, lvalue, rvalue):
		"""
		Revisar si el intervalo es válido
		Regresa True o False
		"""
		if lvalue >= rvalue:
			return False
		return True

	def _show_credits(self):
		'''Mostrar los créditos.'''
		print('Este programa fue hecho por ' 
			'Rodrigo Nevarez Escobar 2020 para la clase de Análisis Númerico.')
		input('Presione cualquier botón para continuar...')
		system('cls')


if __name__ == '__main__':
	# Crea una instancia de la calculadora y despúes correrla
	rc = RootCalculator()
	rc.run_calculator()