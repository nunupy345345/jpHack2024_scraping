from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
import time

app = FastAPI()

# Firebase初期化
cred = credentials.Certificate("jphack2024-firebase-adminsdk-k0m2t-f6ab51cd72.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.get("/")
async def hello():
    return {"message": "hello world!"}
  
@app.get("/add-vote-fields")
async def add_vote_fields():
    try:
        batch_size = 100
        docs_processed = 0
        last_doc = None
        has_more = True
        max_retries = 3
        
        while has_more:
            retry_count = 0
            while retry_count < max_retries:
                try:
                    # クエリの作成
                    query = db.collection('facilities').limit(batch_size)
                    if last_doc:
                        query = query.start_after(last_doc)

                    # ドキュメントの取得
                    docs = query.get()
                    docs_list = list(docs)

                    if not docs_list:
                        has_more = False
                        break

                    # バッチ処理
                    for i in range(0, len(docs_list), batch_size):
                        batch = db.batch()
                        current_batch = docs_list[i:min(i + batch_size, len(docs_list))]

                        for doc in current_batch:
                            doc_ref = db.collection('facilities').document(doc.id)
                            batch.update(doc_ref, {
                                'vote_both': 0,
                            })

                        # バッチのコミット
                        batch.commit()
                        # レート制限を避けるための遅延
                        time.sleep(0.5)

                        docs_processed += len(current_batch)
                        print(f"Processed documents: {docs_processed}")

                    last_doc = docs_list[-1]
                    if len(docs_list) < batch_size:
                        has_more = False

                    break  # 成功した場合、リトライループを抜ける

                except Exception as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise HTTPException(
                            status_code=500,
                            detail=f"Failed after {max_retries} retries: {str(e)}"
                        )
                    print(f"Retry {retry_count} after error: {str(e)}")
                    time.sleep(2)  # リトライ前の待機

        return JSONResponse(
            content={
                "message": "Successfully updated all documents",
                "total_processed": docs_processed
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fatal error occurred: {str(e)}"
        )

# バッチ処理の進行状況を確認するエンドポイント
@app.get("/processing-status")
async def get_processing_status():
    try:
        # 処理済みドキュメント数を取得
        docs = db.collection('facilities').get()
        total_docs = len(list(docs))
        
        # 投票フィールドが追加されたドキュメント数を取得
        docs_with_votes = db.collection('facilities')\
            .where('vote_inside_gate', '>=', 0)\
            .get()
        processed_docs = len(list(docs_with_votes))

        return {
            "total_documents": total_docs,
            "processed_documents": processed_docs,
            "remaining_documents": total_docs - processed_docs
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting status: {str(e)}"
        )