from fastapi import APIRouter, HTTPException, status, Depends
from ..utils.security import get_current_user
from ..models.Journal import JournalBase, JournalCreate, JournalInDB, JournalResponse
from ..config.Config import Journal_collection
from bson import ObjectId

router = APIRouter()

@router.post("/entries", status_code=201)
async def create_entry(entry: JournalCreate, current_user=Depends(get_current_user)):
    new_entry = JournalInDB(
        **entry.dict(),
        user_id = str(current_user.id)
    )
    result = Journal_collection.insert_one(new_entry.dict(by_alias=True))
    return new_entry

@router.get("/entries", status_code=200)
async def get_entries( current_user=Depends(get_current_user)):

    cursor_entry = Journal_collection.find({
        "user_id": str(current_user.id)
    })

    entries = []
    for entry in cursor_entry:
        entry["id"] = str(entry["_id"])
        entry["user_id"] = str(entry["user_id"])
        entry.pop("_id")
        entries.append(entry)
    return entries

@router.get("/entry/{entry_id}", response_model=JournalResponse, status_code=200)
async def get_entry(entry_id: str, current_user=Depends(get_current_user)):

    entry_data = Journal_collection.find_one({
        "_id": entry_id,
        "user_id": str(current_user.id)
    })

    if not entry_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal Entry not found or you do not have access to it"
        )
    entry_data["id"] = str(entry_data["_id"])
    entry_data["user_id"] = str(entry_data["user_id"])
    return JournalResponse(**entry_data)