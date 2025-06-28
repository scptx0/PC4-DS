# Contribuciones de Daren Herrera

## Sprint 1
- 2025-06-23:
    - **Rama feat/state-comparator**
        - Implementé la lógica inicial del script que compara el estado de deseado (`terraform.tfstate`) con el estado real (obtenido con `kubectl`)
            - Commits:
                - `feat(py): (Issue #2) implementar script que compara estado real y deseado` ([d123255](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/commit/d12325547be0a4aee95360acee387b3a2ee2274c))
                - `refactor(py): corregir estilo (PEP8) de script comparador inicial` ([a1da959](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/commit/a1da9594ffcafacd5488ee42017fe1bf17498b5c))

    - Pull request grupal: [#6](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/pull/6)

- 2025-06-24:
    - Realicé el video correspondiente al sprint 1. No hay commit de ello.

## Sprint 2

- 2025-06-27 y 2025-06-28:
    - **Rama feat/reporte-drift**
        - Implementé una mejora para el script que compara los estados. Ahora, se tienen cuenta dos atributos más: `container_name` (deployment) y `type` (service). Además, el reporte se imprime como una tabla ASCII en la terminal.
            - Commits:
                - `feat(py): (Issues #7 #8) comparar más atributos y generar tabla ASCII` ([4aa3df7](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/commit/4aa3df7bd5f33b5fa161252f8e364f4365ba8d0c))
                - `refactor(py): unificar estilo (PEP8) para la mejora de reporte de drift` ([dd6b2c3](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/commit/dd6b2c324d5a863a530530cc11140ecf2657f513))

    - Pull request grupal: [#11](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/pull/11)
    - Realicé el video correspondiente al sprint 2. No hay commit de ello