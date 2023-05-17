def corregir_lista(lista):
    # Unir elementos contiguos que forman una misma cadena
    resultado = []
    if any(";" in string for string in lista):
      i = 0
      while i < len(lista):
          if i == len(lista) - 1:
              resultado.append(lista[i].rstrip(";"))
              i += 1
          elif not lista[i].endswith(";") and not lista[i+1].endswith(";"):
              resultado.append(lista[i] + " " + lista[i+1])
              i += 2
          elif not lista[i].endswith(";") and lista[i+1].endswith(";"):
              resultado.append(lista[i] + " " + lista[i+1].rstrip(";"))
              i += 2
          else:
              resultado.append(lista[i].rstrip(";"))
              i += 1
      return resultado
    elif len(lista) > 1:
      name = lista[0]
      for i in lista[1:]:
        name = name + " " + i
      resultado.append(name)
      return resultado
    elif len(lista) == 1:
      resultado.append(lista[0])
      return resultado