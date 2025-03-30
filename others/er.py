from graphviz import Digraph

# Create a new directed graph
er = Digraph('ER_Diagram', node_attr={'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightyellow'})

# Define entities
entities = [
    ('vendors', 'vendor_id, name, rating, location'),
    ('products', 'product_id, name, price, tags, vendor_id'),
    ('customers', 'customer_id, phone, shipping_address'),
    ('orders', 'order_id, customer_id, status, created_at'),
    ('order_items', 'order_id, product_id, quantity'),
    ('order_logs', 'log_id, order_id, action, details, log_time')
]

# Add entities to graph
for entity, attributes in entities:
    er.node(entity, f'{entity.upper()}\n{attributes}')

# Define relationships
relationships = [
    ('vendors', 'products', '1:N', 'vendor_id'),
    ('customers', 'orders', '1:N', 'customer_id'),
    ('orders', 'order_items', '1:N', 'order_id'),
    ('orders', 'order_logs', '1:N', 'order_id')
]

# Add relationships to graph
for src, dest, rel, attr in relationships:
    er.edge(src, dest, label=f'{rel}\n{attr}')

er
