# Claude Instant v1.2を使ってテキスト生成を行うLambda関数

import boto3
import json

bedrock_runtime = boto3.client('bedrock-runtime')

def lambda_handler(event, context):
    # プロンプトに設定する内容を取得
    query_params = event.get('queryStringParameters', {})
    prompt = query_params.get('prompt')
    formatted_prompt = f"\n\nHuman: {prompt}\n\nAssistant:"

    # 各種パラメーターの指定
    modelId = 'anthropic.claude-instant-v1'
    accept = 'application/json'
    contentType = 'application/json'

    # リクエストBODYの指定
    body = json.dumps({
        "prompt": formatted_prompt,
        "max_tokens_to_sample": 250,
        # "temperature": 0.7,
        # "top_p": 1,
    })

    # Bedrock APIの呼び出し
    response = bedrock_runtime.invoke_model(
    	modelId=modelId,
    	accept=accept,
    	contentType=contentType,
        body=body
    )

    response_body = json.loads(response['body'].read())

    # レスポンスBODYから応答テキストを取り出す
    outputText = response_body.get('completion', '')

    # 出力テキストをLambdaの返り値として返す
    return {
        'statusCode': 200,
        'body': outputText
    }