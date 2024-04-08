from faker import Faker
from apps.campeonatos.models import Campeonato,Grupos



faker=Faker()


class CampeoantoFactory:


    def build_campeonato_JSON(self):
        return{
            'nombre':faker.company(),
            'fecha_inicio':faker.date(),
            'fecha_fin':faker.date(),
            'tipo':'invierno',
            'lugar':faker.address()
        }

    def create_campeoanto(self):
        return Campeonato.objects.create(**self.build_campeonato_JSON())