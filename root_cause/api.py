from fastapi import APIRouter
from root_cause.agent import RootCauseAgent

router = APIRouter()

@router.get("/analyze/{equipment_id}")
async def analyze_equipment(equipment_id: str):
    agent = RootCauseAgent()
    result = agent.analyze_equipment(equipment_id)
    agent.close()
    return result

@router.get("/quick/{equipment_id}")
async def quick_analysis(equipment_id: str):
    agent = RootCauseAgent()
    result = agent.analyze_equipment(equipment_id)
    agent.close()
    
    if 'error' in result:
        return result
    
    return {
        'equipment': equipment_id,
        'root_cause': result['root_cause']['primary'],
        'confidence': result['root_cause']['confidence'],
        'top_recommendation': result['recommendations'][0],
        'severity': result['analysis']['severity']
    }