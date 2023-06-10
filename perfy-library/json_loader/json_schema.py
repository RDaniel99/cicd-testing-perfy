import networkx as nx


class JSONSchema:
    def __init__(self):
        self.json_fields = {}
        self.fields_dependencies = {}
        self.G = nx.DiGraph()

    def add_field(self, json_field):
        self.json_fields[json_field.field_name] = json_field

    def add_dependency(self, field_name, dependent_to):
        if field_name in self.fields_dependencies:
            self.fields_dependencies[field_name].append(dependent_to)
        else:
            self.fields_dependencies[field_name] = [dependent_to]

        self.G.add_edge(dependent_to, field_name)

    def get_fields_in_order_of_completion(self):
        return list(nx.topological_sort(self.G))
