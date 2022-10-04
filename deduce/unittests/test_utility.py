import codecs
import unittest
from unittest.mock import patch

from deduce import utility
from deduce.utility import Annotation


class TestUtilityMethods(unittest.TestCase):
    def test_parse_tag(self):
        tag = "<FORNAMEUNKNOWN Peter>"
        tag_type, text = utility.parse_tag(tag)
        self.assertEqual("FORNAMEUNKNOWN", tag_type)
        self.assertEqual("Peter", text)

    def test_find_name_tags(self):
        annotated_text = (
            "Dit is stukje tekst met daarin de naam <FORNAMEPAT Jan> <SURNAMEPAT Jansen>. De "
            "<PREFIXNAME patient J>. <SURNAMEPAT Jansen> (e: j.jnsen@email.com, t: 06-12345678) is 64 "
            "jaar oud en woonachtig in Utrecht. Hij werd op 10 oktober door arts <FORNAMEUNKNOWN "
            "Peter> <INTERFIXNAME de Visser> ontslagen van de kliniek van het UMCU."
        )
        found_tags = utility.find_tags(annotated_text)
        expected_tags = [
            "<FORNAMEPAT Jan>",
            "<SURNAMEPAT Jansen>",
            "<PREFIXNAME patient J>",
            "<SURNAMEPAT Jansen>",
            "<FORNAMEUNKNOWN Peter>",
            "<INTERFIXNAME de Visser>",
        ]
        self.assertEqual(expected_tags, found_tags)

    def test_get_annotations(self):
        text = (
            "Dit is stukje tekst met daarin de naam <FORNAMEPAT Jan> <SURNAMEPAT Jansen>. De "
            "<PREFIXNAME patient J>. <SURNAMEPAT Jansen> (e: j.jnsen@email.com, t: 06-12345678) is 64 "
            "jaar oud en woonachtig in Utrecht. Hij werd op 10 oktober door arts <FORNAMEUNKNOWN "
            "Peter> <INTERFIXNAME de Visser> ontslagen van de kliniek van het UMCU."
        )
        tags = [
            "<FORNAMEPAT Jan>",
            "<SURNAMEPAT Jansen>",
            "<PREFIXNAME patient J>",
            "<SURNAMEPAT Jansen>",
            "<FORNAMEUNKNOWN Peter>",
            "<INTERFIXNAME de Visser>",
        ]
        expected_annotations = [
            Annotation(39, 42, "FORNAMEPAT", "Jan"),
            Annotation(43, 49, "SURNAMEPAT", "Jansen"),
            Annotation(54, 63, "PREFIXNAME", "patient J"),
            Annotation(65, 71, "SURNAMEPAT", "Jansen"),
            Annotation(185, 190, "FORNAMEUNKNOWN", "Peter"),
            Annotation(191, 200, "INTERFIXNAME", "de Visser"),
        ]
        found_annotations = utility.get_annotations(text, tags)
        self.assertEqual(expected_annotations, found_annotations)

    def test_annotate_text(self):
        annotated_text = (
            "Dit is stukje tekst met daarin de naam <PATIENT Jan Jansen>. De "
            "<PATIENT patient J. Jansen> (e: <URL j.jnsen@email.com>, t: <PHONENUMBER 06-12345678>) "
            "is <AGE 64> jaar oud en woonachtig in <LOCATION Utrecht>. Hij werd op "
            "<DATE 10 oktober> door arts <PERSON Peter de Visser> ontslagen van de kliniek van het "
            "<INSTITUTION umcu>."
        )

        tags = utility.find_tags(annotated_text)
        annotations = utility.get_annotations(annotated_text, tags)
        expected_annotations = [
            Annotation(39, 49, "PATIENT", "Jan Jansen"),
            Annotation(54, 71, "PATIENT", "patient J. Jansen"),
            Annotation(76, 93, "URL", "j.jnsen@email.com"),
            Annotation(98, 109, "PHONENUMBER", "06-12345678"),
            Annotation(114, 116, "AGE", "64"),
            Annotation(143, 150, "LOCATION", "Utrecht"),
            Annotation(164, 174, "DATE", "10 oktober"),
            Annotation(185, 200, "PERSON", "Peter de Visser"),
            Annotation(234, 238, "INSTITUTION", "umcu"),
        ]
        self.assertEqual(expected_annotations, annotations)

    def test_get_annotations_leading_space(self):
        annotated_text = "Overleg gehad met <PERSON Jan Jansen>"
        tags = ["<PERSON Jan Jansen>"]
        annotations = utility.get_annotations(annotated_text, tags, 1)
        self.assertEqual(1, len(annotations))
        self.assertEqual(19, annotations[0].start_ix)

    def test_get_first_non_whitespace(self):
        self.assertEqual(1, utility.get_first_non_whitespace(" Overleg"))

    def test_normalize_value(self):
        ascii_str = "Something about Vincent Menger!"
        value = utility._normalize_value("¡" + ascii_str)
        self.assertEqual(ascii_str, value)

    def test_read_list_unique(self):
        list_name = "input_file_name"
        with patch.object(codecs, "open", return_value=["item", "item"]) as _:
            read_list = utility.read_list(list_name, unique=True)
        self.assertEqual(["item"], read_list)

    def test_read_list_non_unique(self):
        list_name = "input_file_name"
        with patch.object(codecs, "open", return_value=["item", "item"]) as _:
            read_list = utility.read_list(list_name, unique=False)
        self.assertEqual(["item", "item"], read_list)

    def test_flatten_text_all_phi(self):
        text = "<INSTITUTION UMC <LOCATION Utrecht>>"
        flattened = utility.flatten_text_all_phi(text)
        self.assertEqual("<INSTITUTION UMC Utrecht>", flattened)

    def test_flatten_text_all_phi_no_nested(self):
        text = "<PERSON Peter> came today and said he loved the <INSTITUTION UMC>"
        flattened = utility.flatten_text_all_phi(text)
        self.assertEqual(text, flattened)

    def test_flatten_text_all_phi_extra_flat(self):
        text = "<INSTITUTION UMC <LOCATION Utrecht>> is the best hospital in <LOCATION Utrecht>"
        flattened = utility.flatten_text_all_phi(text)
        self.assertEqual(
            "<INSTITUTION UMC Utrecht> is the best hospital in <LOCATION Utrecht>",
            flattened,
        )

    def test_flatten_text_all_phi_extra_nested(self):
        text = "<INSTITUTION UMC <LOCATION Utrecht>> was founded by <PERSON Jan van <LOCATION Apeldoorn>>"
        flattened = utility.flatten_text_all_phi(text)
        self.assertEqual(
            "<INSTITUTION UMC Utrecht> was founded by <PERSON Jan van Apeldoorn>",
            flattened,
        )


if __name__ == "__main__":
    unittest.main()
