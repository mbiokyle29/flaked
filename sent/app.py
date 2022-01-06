from datetime import datetime
from csv import DictReader
from io import StringIO
from operator import attrgetter

from fastapi import FastAPI, File, UploadFile

from sent.models import (
    Climb,
    ClimbingStats,
    ClimbingSummary,
    parse_grade,
)


app = FastAPI(
    title='sent',
    description='API for processing yearly climbing data',
)


@app.post('/send', response_model=ClimbingSummary)
async def send(file: UploadFile = File(...)):
    csv_data = await file.read()
    csv_reader = DictReader(StringIO(csv_data.decode('utf8')))
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

    boulder_problems = [c for c in climbs if all(['boulder' in c.climbing_types, c.result not in {'fell/hung', ''}])]
    hardest_boulder = max(boulder_problems, key=attrgetter('grade')) if len(boulder_problems) > 0 else None

    wall_problems = [c for c in climbs if all(['boulder' not in c.climbing_types, c.result not in {'fell/hung', ''}])]
    hardest_wall = max(wall_problems, key=attrgetter('grade')) if len(wall_problems) > 0 else None

    return ClimbingSummary(
        climbs=climbs,
        stats=ClimbingStats(
            total_feet=sum([c.length for c in climbs if c.length is not None]),
            total_climbs=len(climbs),
            avg_rating=sum([c.community_rating for c in climbs]) / max([1, len(climbs)]),
            hardest_boulder_problem=hardest_boulder,
            hardest_wall_problem=hardest_wall,
        )
    )
