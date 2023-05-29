def convert_bytes(bytes):
    units = {'GB': 1024**3, 'MB': 1024**2, 'KB': 1024}
    for unit in units:
        if bytes >= units[unit]:
            return (round(bytes/units[unit],2), unit)
    # If bytes < 1 KB, return bytes as is and unit as bytes
    return (bytes, 'bytes')


