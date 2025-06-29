# PC4

- **Nombre completo:** Daren Adiel Herrera Romo
- **Correo institucional:** `daren.herrera.r@uni.pe`
- **URL del repositorio grupal:** https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4
- **Rol en el equipo:**
    - Contribuí en la creación de:
        - Issues
        - Tablero Kanban
        - Pull requests
        - Pipeline CI
    - Implementé:
        - `state_comparator.py`
        - `pipeline.sh`
        - `drift_remediation.sh`
    - Me encargué de:
        - Implementar el script de python comparador de estados
        - Implementar un "pipeline" (bash) que simula un drift y lo remedia

## Instrucciones para reproducir el código

Se requiere del archivo terraform `main.tf` y su inicialización para poder ejecutar mi script, así que lo más factible sería realizar las dos primeras instrucciones del README grupal. En resumen:

```bash
# Clonar repositorio
git clone https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4.git
# Instalar dependencias
pip install -r requirements.txt
# Inicializar minikube (herramienta local de k8s)
minikube start
# Configuración de terraform
cd iac
terraform init
terraform apply -auto-approve

cd scripts
python state_comparador.py
bash pipeline.sh
``` 