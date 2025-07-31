from abc import ABC, abstractmethod
import uuid

# -------------------------------------------------
# 1) Interface                                   🡇
# -------------------------------------------------
class Logavel(ABC):
    """Qualquer classe logável DEVE implementar logar_entrada()."""
    @abstractmethod
    def logar_entrada(self):
        pass


# -------------------------------------------------
# 2) Mixins                                      🡇
# -------------------------------------------------
class IdentificavelMixin:
    """Gera um ID único; combine-o com outras classes."""
    def __init__(self):
        self.id = uuid.uuid4()
        # TODO: gerar e armazenar um ID (use uuid.uuid4())~

    def get_id(self):
        return self.id
        # TODO: retornar o ID



class AuditavelMixin:
    """Fornece logs simples ao console."""
    def log_evento(self, evento: str):
        # TODO: imprimir no formato  [LOG] <mensagem>
        print(f" [LOG] <{evento}>")


# -------------------------------------------------
# 3) Classe base Pessoa                          🡇
# -------------------------------------------------
class Pessoa:
    """Classe base para pessoas do sistema."""
    def __init__(self, nome: str, cpf: str):
        self._nome = nome
        self._cpf = cpf
        # TODO: armazenar nome e cpf como atributos protegidos

    @property
    def nome(self):
        # TODO: retornar o nome
        return self.nome
    
    def __str__(self):
        return (f"{self.nome} ({self._cpf})")
        # TODO: "Maria (123.456.789-00)"


# -------------------------------------------------
# 4) Bagagem — classe simples                    🡇
# -------------------------------------------------
class Bagagem:
    def __init__(self, descricao: str, peso: float):
        self.descricao = descricao
        self.peso = peso  # kg
    def __str__(self):
        return f"{self.descricao} – {self.peso} kg"


# -------------------------------------------------
# 5) Passageiro                                  🡇
# -------------------------------------------------
class Passageiro(Pessoa):
    """Herda de Pessoa e possui bagagens."""
    def __init__(self, nome: str, cpf: str):
        super().__init__(nome,cpf)
        self.lista_bag = []
        # TODO: chamar super().__init__ e criar lista vazia de bagagens
        
    def adicionar_bagagem(self, bagagem: Bagagem):
        # TODO: adicionar bagagem à lista
        self.lista_bag.append(bagagem)
        
    def listar_bagagens(self):
        # TODO: imprimir as bagagens
        for x in self.lista_bag:
            print(x)


# -------------------------------------------------
# 6) Funcionario (herança múltipla + mixins)     🡇
# -------------------------------------------------
class Funcionario(Pessoa, IdentificavelMixin, Logavel):
    def __init__(self, nome, cpf, cargo, matricula):
        super().__init__(nome, cpf)
        self._cargo = cargo
        self._matricula = matricula

    def exibir_dados(self):
        print(f"Nome: {self._nome} \nCargo: {self._cargo}\nMatricula: {self._matricula}\nID: {self.id}")

    def logar_entrada(self):
        print(f" [LOG] <O Funcionário {self.nome} entrou no sistema>")

# TODO: Implementar a classe Funcionario
# - Herda de Pessoa, IdentificavelMixin e Logavel (pode usar AuditavelMixin)
# - Atributos: cargo, matricula
# - Métodos:
#   • exibir_dados() → imprime nome, cargo, matrícula e ID
#   • logar_entrada() → registra no log


# -------------------------------------------------
# 7) MiniAeronave                                🡇
# -------------------------------------------------
class MiniAeronave:
    """Objeto da composição dentro de Voo."""
    def __init__(self, modelo: str, capacidade: int):
        # TODO: armazenar modelo e capacidade
        self.modelo = modelo
        self.capacidade = capacidade

    def resumo_voo(self):
        return (f"A mini aeronave de modelo:{self.modelo} tem a capacidade de {self.capacidade} pessoas")
        # TODO: retornar string com modelo e capacidade
        pass


# -------------------------------------------------
# 8) Voo (composição com MiniAeronave)           🡇
# -------------------------------------------------
# TODO: Implementar a classe Voo
# - Atributos: numero_voo, origem, destino, aeronave
# - Listas: passageiros, tripulacao
# - Métodos:
#   • adicionar_passageiro()  (verificar duplicidade e capacidade)
#   • adicionar_tripulante()
#   • listar_passageiros()
#   • listar_tripulacao()


# -------------------------------------------------
# 9) CompanhiaAerea                              🡇
# -------------------------------------------------
class CompanhiaAerea:
    """Agrupa seus voos (has-a)."""
    def __init__(self, nome: str):
        # TODO: validar nome (≥ 3 letras) e criar lista vazia de voos
        pass
    @property
    def nome(self):
        # TODO: retornar nome
        pass
    @nome.setter
    def nome(self, novo_nome: str):
        # TODO: validar + atualizar nome
        pass
    def adicionar_voo(self, voo):
        # TODO: adicionar voo à lista
        pass
    def buscar_voo(self, numero: str):
        # TODO: retornar voo ou None
        pass
    def listar_voos(self):
        # TODO: imprimir todos os voos
        pass


# -------------------------------------------------
# 10) Auditor (Identificável + Logável)          🡇
# -------------------------------------------------
# TODO: Implementar a classe Auditor
# - Herda de IdentificavelMixin e Logavel
# - Atributo: nome
# - Métodos:
#   • logar_entrada() → registra entrada no sistema
#   • auditar_voo(voo) → verifica:
#       ▸ passageiros ≤ capacidade
#       ▸ existe ao menos 1 tripulante
#     imprime relatório de conformidade
#   • __str__() → "Auditor <nome> (ID: ...)"


# -------------------------------------------------
# 11) Bloco de teste                             🡇
# -------------------------------------------------
if __name__ == "__main__":
    """
    TODO:
      • Criar 2 companhias, 2 voos cada, passageiros, funcionários e auditor.
      • Adicionar bagagens, listar passageiros, auditar voos.
      • Mostrar saídas no console para validar implementações.
    """
    pass
