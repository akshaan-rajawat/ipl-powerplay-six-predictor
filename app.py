from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

df = pd.read_csv("ipl_dataset_final_enhanced_v2.csv")
model = joblib.load("ipl_promo_model_v3.pkl")
preprocessor = joblib.load("ipl_preprocessor.pkl")

valid_teams = sorted(set(df['team1']).union(set(df['team2'])))
valid_venues = sorted(df['venue'].unique())

team_venues = {}
for team in valid_teams:
    venues_team1 = set(df[df['team1'] == team]['venue'].unique())
    venues_team2 = set(df[df['team2'] == team]['venue'].unique())
    team_venues[team] = sorted(list(venues_team1.union(venues_team2)))

def get_features(team1, team2, venue):
    return pd.DataFrame([{
        'team1': team1,
        'team2': team2,
        'venue': venue,
        'team1_batsmen_avg_six_pct': df[df['team1'] == team1]['team1_batsmen_avg_six_pct'].mean(),
        'team2_batsmen_avg_six_pct': df[df['team2'] == team2]['team2_batsmen_avg_six_pct'].mean(),
        'venue_six_rate': df[df['venue'] == venue]['venue_six_rate'].mean(),
        'venue_promo_rate': df[df['venue'] == venue]['venue_promo_rate'].mean()
    }]).fillna(df.mean(numeric_only=True))

@app.route('/', methods=['GET'])
def index():
    return render_template(
        'index.html',
        teams=valid_teams,
        venues=valid_venues,
        team_venues=team_venues
    )

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    team1 = data['team1']
    team2 = data['team2']
    venue = data['venue']
    features = get_features(team1, team2, venue)
    prob = model.predict_proba(features)[0][1]
    return jsonify({"result": f"Promo Hit Probability: {prob*100:.1f}%"})

@app.route('/analysis', methods=['POST'])
def analysis():
    top_n = 5
    results = []
    top_venues = valid_venues[:3]
    for i, team1 in enumerate(valid_teams):
        for team2 in valid_teams[i+1:]:
            valid_venues_for_teams = list(set(team_venues.get(team1, []) + team_venues.get(team2, [])))
            for venue in set(valid_venues_for_teams).intersection(top_venues):
                try:
                    features = get_features(team1, team2, venue)
                    prob = model.predict_proba(features)[0][1]
                    results.append((f"{team1} vs {team2} at {venue}", prob))
                except Exception:
                    continue
    results.sort(key=lambda x: x[1], reverse=True)
    best = [f"{i+1}. {m[0]}: {m[1]*100:.1f}%" for i, m in enumerate(results[:top_n])]
    worst = [f"{i+1}. {m[0]}: {m[1]*100:.1f}%" for i, m in enumerate(reversed(results[-top_n:]))]
    return render_template('analysis.html', best=best, worst=worst)

if __name__ == '__main__':
    app.run(debug=True)
