"""
Motor Didático de Mutação em Python via AST (Abstract Syntax Tree).

Este módulo inspeciona o código-fonte de discount_calculator.py,
transforma o AST trocando operadores (ex: > para >=, + para -, or para and)
e executa funções de teste fornecidas para verificar se o mutante é MORTO ou SOBREVIVE.
"""

import ast
import inspect
import types
from typing import Callable, List, Tuple, Any
from discount_calculator import DiscountCalculator, OrderItem



class ASTMutator(ast.NodeTransformer):
    """Transformador AST que substitui operadores por mutantes específicos."""

    def __init__(self, mutation_id: int):
        self.mutation_id = mutation_id
        self.current_id = 0

    def visit_Compare(self, node: ast.Compare) -> ast.AST:
        self.generic_visit(node)
        new_ops = []
        for op in node.ops:
            self.current_id += 1
            if self.current_id == self.mutation_id:
                if isinstance(op, ast.GtE):
                    new_ops.append(ast.Gt())
                elif isinstance(op, ast.Gt):
                    new_ops.append(ast.GtE())
                elif isinstance(op, ast.Eq):
                    new_ops.append(ast.NotEq())
                else:
                    new_ops.append(op)
            else:
                new_ops.append(op)
        node.ops = new_ops
        return node

    def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
        self.generic_visit(node)
        self.current_id += 1
        if self.current_id == self.mutation_id:
            if isinstance(node.op, ast.Sub):
                node.op = ast.Add()
            elif isinstance(node.op, ast.Add):
                node.op = ast.Sub()
        return node

    def visit_BoolOp(self, node: ast.BoolOp) -> ast.AST:
        self.generic_visit(node)
        self.current_id += 1
        if self.current_id == self.mutation_id:
            if isinstance(node.op, ast.Or):
                node.op = ast.And()
            elif isinstance(node.op, ast.And):
                node.op = ast.Or()
        return node


class MutationRunner:
    """Orquestrador que executa suítes de testes contra os mutantes."""

    @staticmethod
    def run_suite_against_calculator(
        calculator_cls: type[DiscountCalculator],
        test_fn: Callable[[type[DiscountCalculator]], None]
    ) -> bool:
        """
        Executa a função de teste fornecida passando a classe do calculador.
        Retorna True se o teste FALHOU (Mutante Morto).
        Retorna False se o teste PASSOU (Mutante Sobreviveu).
        """
        try:
            test_fn(calculator_cls)
            # Se a suíte de testes passou sem lançar exceção, o mutante SOBREVIVEU!
            return False
        except Exception:
            # Se a suíte de testes lançou exceção (AssertionError, etc.), o mutante foi MORTO!
            return True

    @classmethod
    def evaluate_suite_on_mutants(
        cls,
        mutants_dict: dict[str, type[DiscountCalculator]],
        test_fn: Callable[[type[DiscountCalculator]], None]
    ) -> dict[str, Any]:
        """
        Avalia uma suíte de testes em relação a um conjunto de mutantes.
        """
        results = {}
        killed_count = 0
        total_mutants = len(mutants_dict)

        for mutant_name, mutant_cls in mutants_dict.items():
            is_killed = cls.run_suite_against_calculator(mutant_cls, test_fn)
            results[mutant_name] = {
                "killed": is_killed,
                "status": "MORTO 🔴" if is_killed else "SOBREVIVEU 🟢"
            }
            if is_killed:
                killed_count += 1

        mutation_score = (killed_count / total_mutants) * 100.0 if total_mutants > 0 else 0.0

        return {
            "results": results,
            "killed_count": killed_count,
            "total_mutants": total_mutants,
            "mutation_score": mutation_score
        }
