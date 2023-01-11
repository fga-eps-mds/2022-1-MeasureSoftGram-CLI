def get_metric_value(extracted):
    """
    Função que recupera o valor mais recente da métrica
    """
    # Métricas que o parâmetro é uma lista de valores
    listed_values = [
        'coverage', 'complexity', 'functions',
        'comment_lines_density', 'duplicated_lines_density'
    ]
    response_data = {}

    # Para todos os arquivos extraidos
    for path_readed in extracted.values():
        qualifier = path_readed['qualifier']
        measures = path_readed['measures']

        # Para cada métrica dentro das medidas
        for metric in measures:
            metric_name = metric['metric']
            metric_value = metric['value']

            # Se ela for "agregada", olho apenas arquivos FIL,
            # se não, salvo somente a última.
            if metric_name in listed_values and qualifier == 'FIL':
                response_data.setdefault(metric_name, []).append(metric_value)
            elif metric_name not in listed_values:
                response_data[metric_name] = metric_value

    return response_data