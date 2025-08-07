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
        return self._nome
    

    def __str__(self):
        return (f"{self._nome} ({self._cpf})")
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
class Funcionario(Pessoa, IdentificavelMixin, Logavel, AuditavelMixin):
    def __init__(self, nome, cpf, cargo, matricula):
        super().__init__(nome, cpf)
        IdentificavelMixin.__init__(self)
        self._cargo = cargo
        self._matricula = matricula

    def exibir_dados(self):
        print(f"Nome: {self._nome} \nCargo: {self._cargo}\nMatricula: {self._matricula}\nID: {self.id}")

    def logar_entrada(self, evento):
        return super().log_evento(evento)

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


# -------------------------------------------------
# 8) Voo (composição com MiniAeronave)           🡇
# -------------------------------------------------
class Voo:
    def __init__(self, numero_voo, origem, destino, aeronave: MiniAeronave):
        self.modelo = aeronave.modelo
        self.capacidade = aeronave.capacidade
        if len(numero_voo) >= 3:
            self.numero_voo = numero_voo
        else:
            raise ValueError("O número de voo tem que ser maior do que 3 algarismo.")
        self.origem = origem
        self.destino = destino
        self.aeronave = aeronave
        self.passageiros = []
        self.tripulacao = []
    
    def adicionar_passageiro(self,passageiro : Passageiro):
        if passageiro in self.passageiros:
            print("O passageiro já está na aeronave.")

        elif len(self.passageiros) < self.capacidade:
            self.passageiros.append(passageiro)
            print("Passageiro adicionado com sucesso.")

        else:
            print("A aeronave está com o número máximo de passageiros.")


    def adicionar_tripulante(self, tripulante : Funcionario):
        if tripulante in self.tripulacao:
            print(f"O funcionário informado está dentro da aeronave")

        elif not tripulante in self.tripulacao and len(self.tripulacao) < self.capacidade:
            self.tripulacao.append(tripulante)

        else:
            print(f"A aeronave está com o número máximo de tripulantes")

    def listar_passageiros(self):
        for passageiro in self.passageiros:
            print(passageiro.nome)

    def listar_tribulantes(self):
        for tripulante in self.tripulacao:
            print(tripulante.nome)

    def __str__(self):
        return f"Voo {self.numero_voo} de {self.origem} para {self.destino}"


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
        if len(nome) >= 3 :
            self._nome = nome
        else:
            raise ValueError("O nome do voo deve ter mais de 3 letras") 
        self.lista_Voos = []
        # TODO: validar nome (≥ 3 letras) e criar lista vazia de voos

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, novo_nome: str):
        if len(novo_nome) >= 3:
            self._nome = novo_nome
        else:
            raise ValueError("O nome do voo deve ter mais de 3 letras") 
        # TODO: validar + atualizar nome
        
    def adicionar_voo(self, voo):
        if not voo in self.lista_Voos:
            self.lista_Voos.append(voo)
        
        else:
            print(f"O voo: {voo} já foi cadasrtado")
    

    def buscar_voo(self, numero: str):
        for voo in self.lista_Voos:
            if voo.numero_voo == numero:
                return voo
        return None

    def listar_voos(self):
        for voo in self.lista_Voos:
            print(voo)




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
class Auditor(IdentificavelMixin, Logavel, AuditavelMixin):
    def __init__(self, nome: str):
        super().__init__()
        self.nome = nome
    
    def logar_entrada(self, evento="Entrada logada com sucesso!"):
        return super().log_evento(evento)
    
    def auditar_voo(self, voo: Voo):
        if len(voo.passageiros) > voo.capacidade:
            raise ValueError("O número de passageiros é inválido.")
        elif len(voo.passageiros) < 1:
            raise ValueError("O voo deve conter ao menos 1 passageiro a bordo.")
        elif len(voo.tripulacao) < 1:
            raise ValueError("O voo deve conter ao menos um tripulante a bordo")
        else:
            return f"o voo {voo} foi auditorado com sucesso"
    
    def __str__(self):
        return f"Nome do auditor: {self.nome} \nID do auditor: {self.get_id()}"

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

  # ===== Testes para Bagagem e Passageiro =====
print("==== Testando Passageiro e Bagagens ====")
p1 = Passageiro("Maria", "123.456.789-00")
bag1 = Bagagem("Mochila", 5.5)
bag2 = Bagagem("Mala de rodinha", 10.2)
p1.adicionar_bagagem(bag1)
p1.adicionar_bagagem(bag2)
p1.listar_bagagens()

# ===== Testes para Funcionario com Mixins e Logavel =====
print("\n==== Testando Funcionario ====")
f1 = Funcionario("Carlos", "987.654.321-00", "Piloto", "MAT123")
f1.exibir_dados()
f1.logar_entrada("Funcionário entrou no sistema")

# ===== Testes para MiniAeronave e Voo (composição) =====
print("\n==== Testando Voo e MiniAeronave ====")
aeronave = MiniAeronave("Boeing 737", 2)  # Capacidade de 2 para facilitar testes
voo1 = Voo("Boeing 737", 2, "VOO123", "São Paulo", "Rio de Janeiro", aeronave)
print(voo1)

voo1.adicionar_passageiro(p1)
voo1.adicionar_tripulante(f1)
voo1.listar_passageiros()
voo1.listar_tribulantes()

# ===== Testando CompanhiaAerea (agregação) =====
print("\n==== Testando Companhia Aérea ====")
cia = CompanhiaAerea("Latam")
cia.adicionar_voo(voo1)
cia.listar_voos()
voo_buscado = cia.buscar_voo("VOO123")
print("Voo encontrado:", voo_buscado)

# ===== Testando Auditor com IdentificavelMixin e Logavel =====
print("\n==== Testando Auditor ====")
auditor = Auditor("João Auditor")
auditor.logar_entrada()
print(auditor)

# Auditar voo
print("\n==== Auditando Voo ====")
resultado_auditoria = auditor.auditar_voo(voo1)
print(resultado_auditoria)

# ===== Testando erro de validação de voo =====
print("\n==== Testando erros de voo ====")
try:
    voo_invalido = Voo("Airbus", 1, "12", "SP", "RJ", aeronave)  # Número de voo inválido
except ValueError as e:
    print("Erro esperado:", e)

try:
    CompanhiaAerea("Oi")  # Nome muito curto
except ValueError as e:
    print("Erro esperado:", e)

# ===== Teste de duplicidade de voo na companhia =====
print("\n==== Testando duplicidade de voo ====")
cia.adicionar_voo(voo1)  # Deve exibir mensagem de duplicidade
