from data_loader import read_data
import certifi
from py2neo import Graph


class DocumentBase:
    def __init__(self, uri, user, password):
        ca_path = certifi.where()

        self.driver2 = Graph(uri, user=user, password=password)

    def add_authors(self, df):
        tx = self.driver2.begin()
        for index, row in df.iterrows():
            tx.evaluate(
                """
            MERGE (a:Author {name:$author})
            MERGE (d:Document {title:$title,document_id:$document_id})
            MERGE (a)-[:IS_AUTHOR]->(d)
            """,
                parameters={
                    "author": row["Authors"],
                    "title": row["DocumentName"],
                    "document_id": row["DocumentID"],
                },
            )
        self.driver2.commit(tx)

        return

    def add_sections(self, df):
        tx = self.driver2.begin()
        for index, row in df.iterrows():
            tx.evaluate(
                """
            MATCH(d:Document{document_id:$document_id})
            MERGE(s:Section{section_id:$section_id,section_name:$section_name,word_count:$word_count})
            MERGE(d)-[:HAS_SECTION]->(s)
            """,
                parameters={
                    "document_id": row["DocumentID"],
                    "section_id": row["SectionID"],
                    "section_name": row["SectionName"],
                    "word_count": row["WordCount"],
                },
            )
        self.driver2.commit(tx)
        return

    def add_section_refs(self, df):
        tx = self.driver2.begin()
        for index, row in df.iterrows():
            for section_id2 in row["ReferencedSectionIDs"].split(","):
                tx.evaluate(
                    """
                    MATCH (s1:Section{section_id:$section_id1})
                    MATCH (s2:Section{section_id:$section_id2})
                    MERGE (s1)-[:HAS_REFERENCE]->(s2)
                    """,
                    parameters={
                        "section_id1": int(row["SectionID"]),
                        "section_id2": int(section_id2),
                    },
                )
        self.driver2.commit(tx)
        return
