export const MATCH_PREFERENCES = [
  {
    key: 'food_points',
    label: 'Good food',
    shortLabel: 'Food',
    marker: 'FD',
    color: '#de7d33',
  },
  {
    key: 'safety_points',
    label: 'Feeling safe',
    shortLabel: 'Safety',
    marker: 'SF',
    color: '#3b7dcc',
  },
  {
    key: 'respect_points',
    label: 'Being treated with respect',
    shortLabel: 'Respect',
    marker: 'RS',
    color: '#c84672',
  },
  {
    key: 'caring_points',
    label: 'Caring staff',
    shortLabel: 'Caring',
    marker: 'CR',
    color: '#2f9b64',
  },
  {
    key: 'home_points',
    label: 'Feeling comfortable and at home',
    shortLabel: 'At home',
    marker: 'HM',
    color: '#7a5cc7',
  },
  {
    key: 'staffing_points',
    label: 'Enough care staff available',
    shortLabel: 'Staffing',
    marker: 'ST',
    color: '#b16a2d',
  },
  {
    key: 'compliance_points',
    label: 'Strong compliance and safety record',
    shortLabel: 'Compliance',
    marker: 'CP',
    color: '#25877e',
  },
  {
    key: 'clinical_quality_points',
    label: 'Clinical care quality',
    shortLabel: 'Clinical quality',
    marker: 'CQ',
    color: '#5f7486',
  },
]

export function emptyMatchWeights() {
  return MATCH_PREFERENCES.reduce((weights, pref) => {
    weights[pref.key] = 0
    return weights
  }, {})
}
