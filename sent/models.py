from datetime import date
from uuid import UUID
from typing import Optional, List

from pydantic import BaseModel, HttpUrl


CLIMBING_TYPES = ['sport', 'trad', 'alpine', 'ice', 'boulder']
CLIMBING_STYLES = ['solo', 'tr', 'follow', 'lead']
RESULT_TYPES = ['onsight', 'flash', 'redpoint', 'pinkpoint', 'fell/hung']
LETTER_GRADES = ['a', 'b', 'c', 'd']


class Grade(BaseModel):
    base: int
    modifier: int
    raw: str

    def __lt__(self, other):
        return (self.base, self.modifier) < (other.base, other.modifier)


class Climb(BaseModel):
    date: date
    route: str
    grade: Grade
    notes: Optional[str]
    uri: HttpUrl
    pitches: int
    crag: str
    community_rating: float
    your_rating: Optional[float]
    length: Optional[int]
    climbing_types: List[str]
    climbing_style: str
    result: str


def parse_grade(grade):

    if grade.startswith('V'):

        parsed_grade = grade.replace('V', '').split(' ')[0]

        if parsed_grade.endswith('-'):
            return Grade(
                base=int(parsed_grade.split('-')[0]),
                modifier=-1,
                raw=grade,
            )

        elif parsed_grade.endswith('+'):
            return Grade(
                base=int(parsed_grade.split('+')[0]),
                modifier=1,
                raw=grade,
            )

        elif '-' in parsed_grade:
            return Grade(
                base=int(parsed_grade.split('-')[0]),
                modifier=1,
                raw=grade,
            )

        else:
            return Grade(
                base=int(parsed_grade),
                modifier=0,
                raw=grade,
            )

    elif grade.startswith('5.'):

        parsed_grade = grade.replace('5.', '').split(' ')[0]

        if parsed_grade.endswith('-'):
            return Grade(
                base=int(parsed_grade.split('-')[0]),
                modifier=-1,
                raw=grade,
            )

        elif parsed_grade.endswith('+'):
            return Grade(
                base=int(parsed_grade.split('+')[0]),
                modifier=5,
                raw=grade,
            )

        elif '/' in parsed_grade:
            numeric_grade_lower_letter, upper_letter = parsed_grade.split('/')

            numeric_grade = int(numeric_grade_lower_letter[:-1])
            upper_letter = upper_letter.lower()
            lower_letter = numeric_grade_lower_letter[-1].lower()
            modifier = (LETTER_GRADES.index(lower_letter) + LETTER_GRADES.index(upper_letter) + 2) / 2

            return Grade(
                base=numeric_grade,
                modifier=modifier,
                raw=grade,
            )

        elif not str.isdigit(parsed_grade[-1]): 
            numeric_grade = int(parsed_grade[:-1])
            letter_modifier = parsed_grade[-1].lower()

            return Grade(
                base=numeric_grade,
                modifier=LETTER_GRADES.index(letter_modifier) + 1,
                raw=grade,
            )

        else: 
            return Grade(
                base=int(parsed_grade),
                modifier=0,
                raw=grade,
            )
