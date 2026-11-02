
import csv
import json
import pydgraph

# ------------------------
# CONNECTION
# ------------------------
# Conexión a Dgraph (localhost:9080)
client_stub = pydgraph.DgraphClientStub('localhost:9080')
client = pydgraph.DgraphClient(client_stub)


# ------------------------
# SCHEMA
# ------------------------
def create_schema():
    """
    TODO: Define aquí tu schema

    Debes incluir:
    - Tipos: Product, Supplier
    - Tipos de datos correctos
    - SOLO los índices necesarios según las queries

    Considera las relaciones entre Product y Supplier.

    Ejemplo:
    name: string @index(term) .
    """

    schema = """
    """

    # TODO: aplicar schema
    # agregar código para poder cargar el schema

    pass


# ------------------------
# DROP ALL
# ------------------------
def drop_all():
    confirm = input("Esto eliminará TODO el grafo. ¿Continuar? (s/n): ")

    if confirm.lower() == "s":
        # TODO:
        # agregar el código para poder borrar todo el schema y los datos
        print("Grafo eliminado completamente")
    else:
        print("Operación cancelada")


# ------------------------
# GEO HELPER
# ------------------------
def parse_location(location_str):
    """
    Convierte "lon,lat" → formato GeoJSON

    Ejemplo:
    "-99.1332,19.4326" →
    {"type": "Point", "coordinates": [-99.1332, 19.4326]}
    """

    # TODO:
    # 1. separar string por coma
    # 2. convertir a float
    # 3. regresar diccionario

    pass


# ------------------------
# LOAD PRODUCTS
# ------------------------
def load_products():
    txn = client.txn()
    try:
        products = []
        with open("products.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                products.append({
                    "uid": "_:" + row["name"],
                    "dgraph.type": "Product",
                    "name": row["name"],
                    "price": float(row["price"]),
                    "category": row["category"]
                })

        res = txn.mutate(set_obj=products)
        txn.commit()
        print("Productos cargados")
        return res.uids
    finally:
        txn.discard()


# ------------------------
# LOAD SUPPLIERS
# ------------------------
def load_suppliers():
    txn = client.txn()
    try:
        suppliers = []
        with open("suppliers.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                suppliers.append({
                    "uid": "_:" + row["supplier_name"],
                    "dgraph.type": "Supplier",
                    "supplier_name": row["supplier_name"],
                    "location": parse_location(row["location"])
                })

        res = txn.mutate(set_obj=suppliers)
        txn.commit()
        print("Proveedores cargados")
        return res.uids
    finally:
        txn.discard()


# ------------------------
# CREATE RELATIONSHIPS
# ------------------------
def create_edges(product_uids, supplier_uids):
    txn = client.txn()
    try:
        with open("product_supplier.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                txn.mutate(set_obj={
                    "uid": supplier_uids[row["supplier_name"]],
                    "supplies": {
                        "uid": product_uids[row["product_name"]]
                    }
                })

        txn.commit()
        print("Relaciones creadas")
    finally:
        txn.discard()


# ------------------------
# RDF MUTATION (RAW INPUT)
# ------------------------
def run_rdf_mutation():
    print("\n--- MUTACIÓN RDF ---")
    print("Pega tu mutación. Escribe END en una nueva línea para ejecutar:\n")

    lines = []

    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    rdf_mutation = "\n".join(lines)

    txn = client.txn()
    try:
        res = txn.mutate(set_nquads=rdf_mutation)
        txn.commit()
        print("Mutación ejecutada correctamente")
        print("UIDs generados:", res.uids)

    except Exception as e:
        print("Error en mutación:", e)

    finally:
        txn.discard()


# ------------------------
# QUERIES
# ------------------------

# 1. Productos por nombre
def query_products_by_name():
    name = input("Nombre del producto: ")
    query = """
    query q($name: string) {
        products(func: type(Product)) @filter(anyofterms(name, $name)) {
            name
            price
            category
        }
    }
    """
    res = client.txn(read_only=True).query(query, variables={'$name': name})
    print(json.dumps(json.loads(res.json), indent=2))


# 2. Productos por precio (con suppliers)
def query_products_by_price():
    price = input("Precio mínimo: ")

    query = """
    
    """

    # TODO: ejecutar query


# 3. Productos por categoría (con suppliers)
def query_products_by_category():
    category = input("Categoría: ")

    query = """

    """

    # TODO: ejecutar query


# 4. Suppliers con sus productos
def query_suppliers_with_products():
    supplier = input("Nombre del proveedor: ")

    query = """
    
    """

    # TODO: ejecutar query


# ------------------------
# MENU
# ------------------------
def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Crear schema")
        print("2. Cargar datos CSV")
        print("3. Ejecutar queries")
        print("4. Drop All")
        print("5. Mutación RDF (manual)")
        print("6. Salir")

        option = input("Selecciona una opción: ")

        if option == "1":
            create_schema()

        elif option == "2":
            # TODO: llama las funciones para cargar los productos,
            # los suppliers y luego la función para crear las relaciones
            pass

        elif option == "3":
            print("\n--- QUERIES ---")
            print("1. Productos por nombre")
            print("2. Productos por precio")
            print("3. Productos por categoría")
            print("4. Suppliers con sus productos")

            q = input("Selecciona una query: ")

            if q == "1":
                query_products_by_name()
            elif q == "2":
                query_products_by_price()
            elif q == "3":
                query_products_by_category()
            elif q == "4":
                query_suppliers_with_products()

        elif option == "4":
            drop_all()

        elif option == "5":
            run_rdf_mutation()

        elif option == "6":
            break

        else:
            print("Opción inválida")


# ------------------------
# MAIN
# ------------------------
def main():
    menu()


if __name__ == "__main__":
    try:
        main()
    finally:
        client_stub.close()
