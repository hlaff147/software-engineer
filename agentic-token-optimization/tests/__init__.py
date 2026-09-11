"""
Suíte de testes automatizados do Token Router.
Configura o sys.path automaticamente para permitir execução isolada.
"""

import sys
import os

# Garante que 'src' esteja acessível para importação nos testes
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_dir = os.path.join(root_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
