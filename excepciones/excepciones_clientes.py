
class ErrorCliente(Exception):
    """Excepción general para errores relacionados con clientes."""
    pass


class DatosClienteInvalidos(ErrorCliente):
    """Se produce cuando los datos de un cliente no son válidos."""
    pass


class ClienteNoEncontrado(ErrorCliente):
    """Se produce cuando no se encuentra un cliente."""
    pass
