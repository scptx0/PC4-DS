import json
import subprocess
import os

CARPETA_ACTUAL = os.path.abspath(__file__)
CARPETA_RAIZ = os.path.dirname(os.path.dirname(CARPETA_ACTUAL))

NOMBRE_DEPLOYMENT = ""
NOMBRE_SERVICE = ""


def cargar_tfstate(ruta):
    """
    Se carga el estado que se espera, configurado en los archivos .tf (main.tf)

    Parametros:
    - ruta (str): Ruta en donde se encuentra 'terraform.tfstate'
    """
    try:
        with open(ruta) as f:
            return json.load(f)
    except BaseException:
        raise IOError(
            "El archivo no existe o no se pudo abrir. Asegurate de haber ejecutado "
            "'terraform init' + 'terraform apply' en 'iac/'")


def obtener_estado_deseado(tfstate):
    """
    Se obtiene el estado deseado a partir del archivo 'terraform.tfstate'

    Parametros:
    - tfstate (dict): JSON que contiene el estado deseado de la infraestuctura

    Retorna:
    - estado (dict): Diccionario que contiene dos diccionarios, uno para el deployment,
    y otro para el service, ambos con los valores deseados de los atributos.
    """
    estado = {}

    global NOMBRE_DEPLOYMENT, NOMBRE_SERVICE

    # Se extraen los atributos del estado en el que deseamos que esté nuestra
    # infraestructura (terraform.tfstate)
    for recurso in tfstate["resources"]:
        if recurso["type"] == "kubernetes_deployment":
            atributos = recurso["instances"][0]["attributes"]
            container = atributos["spec"][0]["template"][0]["spec"][0]["container"][0]

            estado["deployment"] = {
                "replicas": atributos["spec"][0]["replicas"],
                "image": container["image"],
                "container_port": container["port"][0]["container_port"]
            }

            NOMBRE_DEPLOYMENT = atributos["metadata"][0]["name"]

        elif recurso["type"] == "kubernetes_service":
            atributos = recurso["instances"][0]["attributes"]
            port = atributos["spec"][0]["port"][0]

            estado["service"] = {
                "port": port["port"],
                "target_port": port["target_port"]
            }

            NOMBRE_SERVICE = atributos["metadata"][0]["name"]

    return estado


def obtener_estado_real():
    """
    Se obtiene el estado real del cluster ejecutando 'kubectl get -o json'.

    Retorna:
    - estado (dict): Diccionario que contiene dos diccionarios, uno para el deployment, y
    otro para el service, ambos con los valores reales de los atributos.
    """
    estado = {}

    # Se obtiene el estado real del Deployment con kubectl
    resultado_deployment = subprocess.run(
        [
            "kubectl",
            "get",
            "deployment",
            NOMBRE_DEPLOYMENT,
            "-o",
            "json"],
        capture_output=True,
        text=True)
    try:
        estado_deployment = json.loads(resultado_deployment.stdout)
    except BaseException:
        raise json.JSONDecodeError(
            "Salida inválida de kubectl. Asegurate de haber ejecutado 'minikube start'")

    estado["deployment"] = {
        "replicas": estado_deployment["spec"]["replicas"],
        "image": estado_deployment["spec"]["template"]["spec"]["containers"][0]["image"],
        "container_port": estado_deployment["spec"]["template"]["spec"]["containers"][0]
        ["ports"][0]["containerPort"]
    }

    # Se obtiene el estado real del Service con kubectl
    resultado_service = subprocess.run(["kubectl",
                                        "get",
                                        "service",
                                        NOMBRE_SERVICE,
                                        "-o",
                                        "json"],
                                       capture_output=True,
                                       text=True)
    try:
        estado_service = json.loads(resultado_service.stdout)
    except BaseException:
        raise json.JSONDecodeError(
            "Salida inválida de kubectl. Asegurate de haber ejecutado 'minikube start'")

    estado["service"] = {
        "port": estado_service["spec"]["ports"][0]["port"],
        "target_port": estado_service["spec"]["ports"][0]["targetPort"]
    }

    return estado


def comparar(estado_deseado, estado_real):
    """
    Se imprime la comparación entre los atributos del deployment (replicas, image,
    container_port) y del service (port, target_port).

    Parámetros:
    - estado_deseado (dict): Diccionario con los atributos y sus valores deseados.
    - estado_real (dict): Diccionario con los atributos y sus valores reales.
    """
    print("\nComparación de atributos del Deployment:")
    for clave in ["replicas", "image", "container_port"]:
        valor_deseado = estado_deseado["deployment"].get(clave)
        valor_real = estado_real["deployment"].get(clave)

        if str(valor_deseado) != str(valor_real):
            print(
                f"Drift en {clave}: El valor deseado es {valor_deseado}"
                f" y el valor real es {valor_real}")
        else:
            print(f"No hay drift para {clave}. El valor es {valor_real}.")

    print("\nComparación de atributos del Service:")
    for clave in ["port", "target_port"]:
        valor_deseado = estado_deseado["service"].get(clave)
        valor_real = estado_real["service"].get(clave)

        if str(valor_deseado) != str(valor_real):
            print(
                f"Drift en {clave}: El valor deseado es {valor_deseado}"
                f" y el valor real es {valor_real}")
        else:
            print(f"No hay drift para {clave}. El valor es {valor_real}.")


if __name__ == "__main__":
    tfstate = cargar_tfstate(
        os.path.join(
            CARPETA_RAIZ,
            "iac/terraform.tfstate"))
    estado_deseado = obtener_estado_deseado(tfstate)
    estado_real = obtener_estado_real()
    comparar(estado_deseado, estado_real)
