def total_vendas(vendas):
    """Retorna o total vendido a partir de uma lista de vendas."""
    return sum(vendas)


def ticket_medio(vendas):
    """Retorna o ticket médio (valor cheio, sem arredondar)."""
    return sum(vendas) / len(vendas)


def status_meta(vendas, meta):
    """Retorna se o total de vendas bateu a meta."""
    if total_vendas(vendas) >= meta:
        return "Bateu a meta"
    else:
        return "Nao bateu a meta"