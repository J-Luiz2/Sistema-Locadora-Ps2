from models import Obra, Emprestimo, Usuario
from datetime import timedelta,date
from rich.table import Table
from rich.console import Console
console = Console()



class Acervo:
    def _relatorio_builder(self, titulo):
        """Relatorio Buider
        Args: Titulo
        
        Returns: Instância de Relatorio Buider"""
        return self._RelatorioBuilder(titulo)
    

    class _RelatorioBuilder:
        def __init__(self, titulo) -> None:
            self.table = Table( title=titulo, show_lines=True)

        def add_header(self, *headers):
            """Add header
            Args: hearders, coloca quantos argumentos quiser em ordem
            
            Returns: table"""
            for cabecalho in headers:
                self.table.add_column(cabecalho, justify='center', style='cyan')

            return self

        def add_linha(self, *rows):
            """Add row
            Args: rows, coloca quantos argumentos quiser em ordem
            
            Returns: table"""
            self.table.add_row(*rows)

            return self

    def __init__(self):
        self.dict_Obras = {}
        self.list_Obras = []
        self.emprestimos = []
        self.historico_emprestimos = []

    def __iadd__(self, obra: Obra):
        '''Adiciona obra
        Args: 
            obra: pertence a class Obra
        
        Returns:
            Adiciona um na quantidade da obra e adiciona na lista do estoque'''
        if str(obra.id) in self.dict_Obras:
            self.dict_Obras[str(obra.id)] += 1
        else:
            self.dict_Obras[str(obra.id)] = obra.quanti
            self.list_Obras.append(obra)
        return self


    def __isub__(self, Obra : Obra):
        '''Remove obra
        Args: 
            obra: pertence a class Obra
        
        Returns:
            Subtrai um na quantidade da obra e remova da lista do estoque 
            se a quantidade for 0'''
        
        if str(Obra.id) in self.dict_Obras and self.dict_Obras[str(Obra.id)] > 1:
            self.dict_Obras[str(Obra.id)] -= 1
        
        elif str(Obra.id) not in self.dict_Obras:
            raise ValueError(f"Não temos a {Obra.titulo} no estoque")
        
        else:
           del self.dict_Obras[str(Obra.id)]
           self.list_Obras.remove(Obra)
        return self
    

    def adicionar(self, Obra: Obra, x = 1):
        '''Adiciona obra
        Args: 
            obra: pertence a class Obra
        
        Returns:
            Adiciona um na quantidade da obra e adiciona na lista do estoque'''
        
        if str(Obra.id) in self.dict_Obras and x >= 1:
            Obra.quanti += x
            self.dict_Obras[str(Obra.id)] = Obra.quanti

        elif x < 1:
            raise ValueError('Somente número naturais acima de 1 são aceitos')
        elif x >= 1:
            Obra.quanti += x
            self.dict_Obras[str(Obra.id)] = Obra.quanti
            self.list_Obras.append(Obra)
        return self
    

    def remover(self, Obra: Obra, x = 1):
        '''Remove obra
        Args: 
            obra: pertence a class Obra
        
        Returns:
            Subtrai um na quantidade da obra e remova da lista do estoque 
            se a quantidade for 0'''
        
        if str(Obra.id) in self.dict_Obras and self.dict_Obras[str(Obra.id)] - x > 1 and x >= 1:
            Obra.quanti -= x
            self.dict_Obras[str(Obra.id)] = Obra.quanti
        
        if str(Obra.id) not in self.dict_Obras:
            raise ValueError(f"Não temos a {Obra.titulo} no estoque")
        
        if x < 1:
            raise ValueError('Somente número naturais acima de 1 são aceitos')
        
        if str(Obra.id) in self.dict_Obras and self.dict_Obras[str(Obra.id)] - x == 0 and x >= 1:
           del self.dict_Obras[str(Obra.id)]
           self.list_Obras.remove(Obra)

        return self
    
    
    
    def emprestar(self, Obra : Obra, Usuario : Usuario, dias =  7):
        """Emprestar
            Args: Obra, Usuario, dias que tem padrão 7
            
            returns: Uma instância da Classe Emprestimo"""

        data_atual = date.today()
        data_prev_devol = data_atual + timedelta(days = dias)
        
        if str(Obra.id) in self.dict_Obras:
            self.remover(Obra)
            emp = Emprestimo(Obra, Usuario, data_atual, data_prev_devol)
            self.emprestimos.append(emp)
            self.historico_emprestimos.append(emp)
            return emp
        
        else:
            raise ValueError(f'A obra({Obra.titulo}) está em falta no estoque')

    def devolver(self, Emprestimo : Emprestimo, data_dev): 
        """Devolver
        Args: Emprestimo, data de devolução
        
        Returns: instância de Emprestimos, Data de devolução"""
        data_dev_date = Emprestimo.transformar_em_date(data_dev)
        Emprestimo.marcar_devolucao(data_dev_date)
        Obra = Emprestimo.obra
        self.adicionar(Obra)
        self.emprestimos.remove(Emprestimo)
        

    def renovar(self, Emprestimo : Emprestimo, dias_extra : int):
        """Renovar
        Args: Instância de Emprestimo, Dias_extra sendo Int
        
        Returns: none, aumenta o prazo da devolução em dias"""

        if dias_extra > 0:
            Emprestimo.data_prev_devol += timedelta(days = dias_extra)

    def valor_multa(self, Emprestimo : Emprestimo, data_ref):
        """Valor Multa
        Args: Instância de Emprestimo, data referida em datetime
        
        Returns: multa em float ou valuerror se a diferença de dias for menor que 1"""
        data_ref_date = Emprestimo.transformar_em_date(data_ref)

        dias_atraso = (data_ref_date - Emprestimo.data_prev_devol).days

        if dias_atraso > 1:
            multa = dias_atraso * 1.00
            return multa
        
        else:
            return 0.0

    
    def relatorio_inventario(self):
        """Relatorio Inventario
        Args: Self
        
        Returns: Tabela"""

        table = self._relatorio_builder('Relatório Iventário')
        for col in ('titulo', 'Autor', 'Ano', 'Categoria', 'Quantidade'):
            table.add_header(col)

        for jogo in self.list_Obras:
            table.add_linha(jogo.titulo, jogo.desenvolvedores , str(jogo.ano), jogo.categoria, str(jogo.quanti))

        return table.table
    
    def historico_debitos(self):
        """Historico Debitos
        Args: self
        
        Returns: Tabela"""
        table = self._relatorio_builder('Historico Débito')

        for col in ('Usuario', 'Obra', 'Valor multa', 'Dias Atrasos'):
            table.add_header(col)

        data_ref = date.today() 
        for emp in self.emprestimos:
            if emp.dias_atraso(data_ref) == 0:
                multa = 0
            
            elif emp.dias_atraso(data_ref) >= 0:
                multa = self.valor_multa(emp, data_ref)

            table.add_linha(emp.usuario.nome, emp.obra.titulo, str(multa), str(emp.dias_atraso(data_ref)))

        return table.table
    
    def historico_debitos_prev(self, data_prev):
        """Historico Debitos previsão
        Args: self
            Data prevista
        
        Returns: Tabela"""
        empre = self.emprestimos[0]

        data_prev_date = empre.transformar_em_date(data_prev)

        data_prev_text = data_prev_date.strftime('%d/%m/%Y')

        table = self._relatorio_builder(f'Historico Débito para Data: ({data_prev_text})')

        for col in ('Usuario', 'Obra', 'Valor multa', 'Dias Atrasos'):
            table.add_header(col)

        for emp in self.emprestimos:
            if emp.dias_atraso(data_prev_date) == 0:
                multa = 0
            
            elif emp.dias_atraso(data_prev_date) >= 0:
                multa = self.valor_multa(emp, data_prev_date)

            table.add_linha(emp.usuario.nome, emp.obra.titulo, str(multa), str(emp.dias_atraso(data_prev_date)))

        return table.table


    def historico_usuario(self, Usuario : Usuario):
        """Exibe o histórico de empréstimos e devoluções de um usuário específico.
          Args: usuario (Usuario): Usuário cujo histórico será exibido.
        Returns:  Table: Objeto da tabela gerada. """
        tabela = self._relatorio_builder(f"Histórico de {Usuario}")
        
        for col in ('Obra', 'Data Retirada', 'Data Prevista Devolução', 'Data Devolução'):
            tabela.add_header(col)

        historico = [emp for emp in self.historico_emprestimos if emp.usuario == Usuario]

        if not historico:
            console.print(f"Nenhum histórico encontrado para o usuário {Usuario}.")
            return tabela.table
        
        for emp in historico:
            data_dev_real = emp.data_dev_real.strftime('%d/%m/%Y') if emp.data_dev_real else "-"
            tabela.add_linha(emp.obra.titulo,
                           emp.data_ret.strftime('%d/%m/%Y'),
                           emp.data_prev_devol.strftime('%d/%m/%Y'),
                            data_dev_real
            )

        return tabela.table

    def _valida_obra(self, obra):
        """Valida Obra
        Args: Instância de Obra
        
        Returns: se a instância é de Obra ou não"""
        if not isinstance(obra, Obra):
            raise TypeError(f'A instância informada não pertence à Classe Obra')
