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
