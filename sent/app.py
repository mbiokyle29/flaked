from datetime import datetime
from csv import DictReader
from io import StringIO
from operator import attrgetter

from fastapi import FastAPI, File, UploadFile

from sent.models import Climb, parse_grade


app = FastAPI(title='sent')


@app.post('/send')
def send(file: UploadFile = File(...)):
    csv_reader = DictReader(StringIO(file.file.read().decode('utf8')))
    climbs = [
        Climb(
            date=datetime.strptime(rec['Date'], '%Y-%m-%d').date(),
            route=rec['Route'],
            grade=parse_grade(rec['Rating']),
            notes=rec['Notes'] if rec['Notes'] != '' else None,
            uri=rec['URL'],
            pitches=int(rec['Pitches']),
            crag=rec['Location'],
            community_rating=float(rec['Avg Stars']),
            your_rating=float(rec['Your Stars']) if rec['Your Stars'] != '-1' else None,
            climbing_style=rec['Style'].lower(),
            climbing_types=[climbing_type.strip().lower() for climbing_type in rec['Route Type'].split(',')],
            result=rec['Lead Style'].lower(),
            length=int(rec['Length']) if rec['Length'] != '' else None,
        )
        for rec in csv_reader
    ]

    return {
        'climbs': [c.dict() for c in climbs],
        'stats': {
            'total_feet': sum([c.length for c in climbs if c.length is not None]),
            'total_climbs': len(climbs),
            'avg_rating': sum([c.community_rating for c in climbs]) / max([1, len(climbs)]),
            'hardest_boulder_problem': max(
                [c for c in climbs if all(['boulder' in c.climbing_types, c.result not in {'fell/hung', ''}])],
                key=attrgetter('grade'),
            ),
            'hardest_wall_problem': max(
                [c for c in climbs if all(['boulder' not in c.climbing_types, c.result not in {'fell/hung', ''}])],
                key=attrgetter('grade'),
            )
        }
    }
