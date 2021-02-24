
class removeBarraN():

    def get(self,texto):
        atv_titulo = texto.split('\n')
        atv_titulo = map(str.strip,atv_titulo)
        atv_titulo= " ".join(atv_titulo).strip()
        return atv_titulo