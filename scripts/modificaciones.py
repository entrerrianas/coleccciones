def sacar_acento(letra):
    """
    Función para devolver una letra sin acentro si lo tiene
    """
    letras_con_acento = {'Á':'A', 'É':'E', 'Í':'I', 'Ó':'O', 'Ú':'U'}
    return letra if letra not in letras_con_acento else letras_con_acento[letra]



    
