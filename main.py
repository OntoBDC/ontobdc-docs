import os
import rdflib

def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    for the mkdocs-macros plugin.
    """
    
    @env.macro
    def get_rdf_exceptions():
        """
        Reads the RDF ontology and returns a list of exceptions.
        For now, this is a mock or queries a specific RDF file.
        You can expand this SPARQL query based on your ontology model.
        """
        # Define the path to the RDF file (relative to this main.py)
        # Adjust the path to wherever your actual ontology/exceptions RDF is stored
        base_dir = os.path.dirname(os.path.abspath(__file__))
        rdf_file = os.path.join(base_dir, 'ontology', 'exceptions.rdf')
        
        exceptions = []
        
        # If the file doesn't exist yet, return a placeholder or empty list
        if not os.path.exists(rdf_file):
            return [
                {
                    "code": "org.ontobdc.domain.resource.document.exception.repository_not_configured",
                    "description": "File repository not configured for capability",
                    "python_type": "ValueError"
                }
            ]
            
        g = rdflib.Graph()
        try:
            g.parse(rdf_file)
            
            # Example SPARQL query - adapt to your actual RDF schema
            qres = g.query(
                """
                PREFIX ontobdc: <http://ontobdc.org/ontology#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                
                SELECT ?code ?description ?pyType
                WHERE {
                   ?ex a ontobdc:Exception ;
                       ontobdc:code ?code ;
                       ontobdc:pythonType ?pyType ;
                       rdfs:comment ?description .
                }
                """
            )
            
            for row in qres:
                exceptions.append({
                    "code": str(row.code),
                    "description": str(row.description),
                    "python_type": str(row.pyType)
                })
        except Exception as e:
            exceptions.append({
                "code": "Error parsing RDF",
                "description": str(e),
                "python_type": "Exception"
            })
            
        return exceptions

    @env.macro
    def render_ontology(file_path):
        """
        Parses an ontology file and renders it as collapsible markdown cards.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        rdf_file = os.path.join(base_dir, file_path)
        
        if not os.path.exists(rdf_file):
            return f"**Error**: Ontology file `{file_path}` not found."
            
        g = rdflib.Graph()
        try:
            fmt = "turtle" if rdf_file.endswith(".ttl") else "xml"
            g.parse(rdf_file, format=fmt)
            
            query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT DISTINCT ?subject ?type ?title ?desc ?id
            WHERE {
               ?subject rdf:type ?type .
               
               # Only get major entities (Capabilities, Exceptions, Parameters)
               FILTER (?type != owl:NamedIndividual && ?type != owl:Class && ?type != owl:Ontology)
               
               OPTIONAL { ?subject dcterms:title | rdfs:label ?title }
               OPTIONAL { ?subject dcterms:description | rdfs:comment ?desc }
               OPTIONAL { ?subject dcterms:identifier ?id }
            }
            ORDER BY ?type ?title
            """
            
            qres = g.query(query)
            
            output = []
            for row in qres:
                subj_uri = str(row.subject)
                subj_name = subj_uri.split('#')[-1] if '#' in subj_uri else subj_uri.split('/')[-1]
                
                type_uri = str(row.type)
                type_name = type_uri.split('#')[-1] if '#' in type_uri else type_uri.split('/')[-1]
                
                title = str(row.title) if row.title else subj_name
                desc = str(row.desc) if row.desc else "No description available."
                identifier = str(row.id) if row.id else subj_uri
                
                card = f"??? note \"{type_name}: {title}\"\n"
                card += f"    **Identifier**: `{identifier}`\n\n"
                card += f"    **Description**: {desc}\n\n"
                card += f"    **URI**: [{subj_name}]({subj_uri})\n"
                output.append(card)
                
            if not output:
                return f"*No renderable entities found in {file_path}.*"
                
            return "\n\n".join(output)
            
        except Exception as e:
            return f"**Error parsing {file_path}**: {str(e)}"
