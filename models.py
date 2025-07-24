import uuid
from datetime import datetime,timedelta,date

class BaseEntity:
    def __init__(self):
        self.id = self._gerar_id
        data_atual = date.today()
        self.data_criacao = data_atual
        

    def __eq__(self, other):
        """__eq__
        Args: Other
        
        Returns: True se other for igual a essa instância e false se não"""
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id


    def _gerar_id(self):
        """Gerar id
        Args: self
        
        Returns: O uuid4 desta instância"""
        return uuid.uuid4()
    
class Jogo(BaseEntity):
    def __init__(self, titulo, ano, categoria, quantidade = 1, *desenvolvedores) :
        self.titulo = titulo
            
        desenvolvedor = ", ".join(desenvolvedores)
        self.desenvolvedores = desenvolvedor
        self.ano = ano
        self.categoria = categoria
        self.quanti = quantidade
        super().__init__()

    def disponivel(self, estoque):
        """Disponivel
        Args: Estoque
        
        returns: True se estiver no estoque ou False se não estiver"""
        if self.id in estoque:
            return True
        else:
            return False
 
        
    def __str__(self):
        """Str
        Args: Self
        
        Returns: String organizada da Obra {Titulo, Ano}"""
        return f'{self.titulo} ({self.ano}).'


class Usuario(BaseEntity):
    def __init__(self, nome, email):
        super().__init__()
        self.nome = nome
        self.email = email

    def __lt__(self, other):
        """Lt
        Args: Intância de Usuario
        
        Returns: Retorna os Usuarios em ordem alfabetica"""
        return self.nome < other.nome



    def __str__(self):
        """Str
        Args: self
        
        Returns: Retorna o Nome do usuario"""
        return self.nome

    
class Emprestimo(BaseEntity):
    def __init__(self, obra: Jogo, usuario: Usuario, data_retirada=None, data_prev_devol=None):
        super().__init__()
        if data_retirada is None:
            data_retirada = date.today()
        if data_prev_devol is None:
            data_prev_devol = data_retirada + timedelta(days=7)

        self.obra = obra
        self.usuario = usuario
        self.data_ret = self.transformar_em_date(data_retirada)
        self.data_prev_devol = self.transformar_em_date(data_prev_devol)
        self.data_dev_real = None


    def transformar_em_date(self, data):
        """Transformar em date
        Args: Valor em date, datetime ou string
        
        Returns: Retorna o valor em date"""
        if isinstance(data, date) and not isinstance(data, datetime):
            
            return data
        elif isinstance(data, datetime):
            
            return data.date()
        elif isinstance(data, str):
            try:
                return datetime.strptime(data, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError("Data em string deve estar no formato 'dd/mm/aaaa'")
        else:
            raise TypeError("Tipo não suportado. Use str, datetime.date ou datetime.datetime.")


    def marcar_devolucao(self, data_dev_real):
        """Marcar
        Args: Data de devolução real em date
        
        Returns: Transforma o argumento em atributo da classe"""
        self.data_dev_real = self.transformar_em_date(data_dev_real)


    def dias_atraso(self, data_ref):
        """Dias atraso
        Args: Data referenciada
        
        Returns: Retorna os dias de atraso"""
        data_ref_date = self.transformar_em_date(data_ref)

        if self.data_dev_real is not None:
            atraso = (self.data_dev_real - self.data_prev_devol).days
        else:
            atraso = (data_ref_date - self.data_prev_devol).days
        
        return max(0, atraso)



    def __str__(self):
        """Str
        Args: Self
        
        Returns: transforma a data prevista de devolução em string e a retorna"""
        data_dev = self.data_prev_devol.strftime("%d/%m/%Y")
        return f'(prev:{data_dev})'
