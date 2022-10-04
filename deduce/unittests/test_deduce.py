import unittest
from unittest.mock import patch

import deduce
from deduce.utility import Annotation


class TestDeduceMethods(unittest.TestCase):
    def test_annotate_text(self):

        text = (
            u"Dit is stukje tekst met daarin de naam Jan Jansen. De patient J. Jansen "
            u"(e: j.jnsen@email.com, t: 06-12345678) is 64 jaar oud en woonachtig in Utrecht. Hij werd op 10 "
            u"oktober door arts Peter de Visser ontslagen van de kliniek van het UMCU."
        )

        annotated = deduce.annotate_text(
            text, patient_first_names="Jan", patient_surname="Jansen"
        )

        expected_text = (
            "Dit is stukje tekst met daarin de naam <PATIENT Jan Jansen>. De <PATIENT patient J. Jansen> "
            "(e: <URL j.jnsen@email.com>, t: <PHONENUMBER 06-12345678>) is <AGE 64> jaar oud en "
            "woonachtig in <LOCATION Utrecht>. Hij werd op <DATE 10 oktober> door arts "
            "<PERSON Peter de Visser> ontslagen van de kliniek van het <INSTITUTION UMCU>."
        )
        self.assertEqual(expected_text, annotated)

    def test_annotate_text_structured(self):
        text = (
            u"Dit is stukje tekst met daarin de naam Jan Jansen. De patient J. Jansen "
            u"(e: j.jnsen@email.com, t: 06-12345678) is 64 jaar oud en woonachtig in Utrecht. Hij werd op 10 "
            u"oktober door arts Peter de Visser ontslagen van de kliniek van het UMCU."
        )
        annotated_text = (
            "Dit is stukje tekst met daarin de naam <PERSON Jan Jansen>. De "
            "<PERSON patient J. Jansen> (e: <URL j.jnsen@email.com>, t: <PHONENUMBER 06-12345678>) "
            "is <AGE 64> jaar oud en woonachtig in <LOCATION Utrecht>. Hij werd op "
            "<DATE 10 oktober> door arts <PERSON Peter de Visser> ontslagen van de kliniek van het "
            "<INSTITUTION umcu>."
        )
        mock_tags = [
            "<PERSON Jan Jansen>",
            "<PERSON patient J. Jansen>",
            "<URL j.jnsen@email.com>",
            "<PHONENUMBER 06-12345678>",
            "<AGE 64>",
            "<LOCATION Utrecht>",
            "<DATE 10 oktober>",
            "<PERSON Peter de Visser>",
            "<INSTITUTION umcu>",
        ]
        mock_annotations = [
            Annotation(39, 49, "PATIENT", "Jan Jansen"),
            Annotation(62, 71, "PATIENT", "J. Jansen"),
            Annotation(76, 93, "URL", "j.jnsen@email.com"),
            Annotation(98, 109, "PHONENUMBER", "06-12345678"),
            Annotation(114, 116, "AGE", "64"),
            Annotation(143, 150, "LOCATION", "Utrecht"),
            Annotation(164, 174, "DATE", "10 oktober"),
            Annotation(185, 200, "PERSON", "Peter de Visser"),
            Annotation(234, 238, "INSTITUTION", "umcu"),
        ]

        def mock_annotate_text(
            mock_text: str,
            patient_first_names="",
            patient_initials="",
            patient_surname="",
            patient_given_name="",
            names=True,
            locations=True,
            institutions=True,
            dates=True,
            ages=True,
            patient_numbers=True,
            phone_numbers=True,
            urls=True,
            flatten=True,
        ):
            return annotated_text if mock_text == text else ""

        def mock_find_tags(tt):
            return mock_tags if tt == annotated_text else []

        def mock_get_annotations(ttext, ttags, tn):
            return (
                mock_annotations
                if ttext == annotated_text and ttags == mock_tags and tn == 0
                else []
            )

        def mock_get_first_non_whitespace(tt):
            return 0 if tt == text else -1

        with patch.object(
            deduce.deduce, "annotate_text", side_effect=mock_annotate_text
        ) as _:
            with patch.object(
                deduce.utility, "find_tags", side_effect=mock_find_tags
            ) as _:
                with patch.object(
                    deduce.utility, "get_annotations", side_effect=mock_get_annotations
                ) as _:
                    with patch.object(
                        deduce.utility,
                        "get_first_non_whitespace",
                        side_effect=mock_get_first_non_whitespace,
                    ) as _:
                        structured = deduce.deduce.annotate_text_structured(
                            text, patient_first_names="Jan", patient_surname="Jansen"
                        )
        self.assertEqual(mock_annotations, structured)

    def test_leading_space(self):
        text = "\t Vandaag is Jan gekomen"
        annotations = deduce.annotate_text_structured(
            text, "Jan", "J.", "Janssen", "Jantinus"
        )
        self.assertEqual(1, len(annotations))
        self.assertEqual(Annotation(13, 16, "PATIENT", "Jan"), annotations[0])

    def test_has_nested_tags_true(self):
        text = "<PERSON Peter <INSTITUTION Altrecht>>"
        self.assertTrue(deduce.deduce.has_nested_tags(text))

    def test_has_nested_tags_false(self):
        text = "<PERSON Peter> from <INSTITUTION Altrecht>"
        self.assertFalse(deduce.deduce.has_nested_tags(text))

    def test_has_nested_tags_error(self):
        text = "> Peter from Altrecht"
        self.assertRaises(ValueError, lambda: deduce.deduce.has_nested_tags(text))

    def test_merge_adjacent_tags(self):
        text = "<PATIENT Jorge><PATIENT Ramos>"
        self.assertEqual(
            "<PATIENT JorgeRamos>", deduce.deduce.merge_adjacent_tags(text)
        )

    def test_do_not_merge_adjacent_tags_with_different_categories(self):
        text = "<PATIENT Jorge><LOCATION Ramos>"
        self.assertEqual(text, deduce.deduce.merge_adjacent_tags(text))

    def test_merge_almost_adjacent_tags(self):
        text = "<PATIENT Jorge> <PATIENT Ramos>"
        self.assertEqual(
            "<PATIENT Jorge Ramos>", deduce.deduce.merge_adjacent_tags(text)
        )


if __name__ == "__main__":
    unittest.main()
