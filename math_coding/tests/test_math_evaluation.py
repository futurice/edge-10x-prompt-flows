from promptflow.client import PFClient

def test_math_evaluation_flow():
    # Initialize the Promptflow client
    pf = PFClient()
    
    # Path to your flow
    flow_path = "../flows/math_evaluation_flow"
    
    # Test case 1: Correct prediction
    result1 = pf.test(flow=flow_path, inputs={
        "groundtruth": "3.14",
        "prediction": "3.14"
    })
    print("\nTest 1 - Exact match:")
    print(f"Score: {result1['score']}")
    
    # Test case 2: Close enough prediction (rounds to same value)
    result2 = pf.test(flow=flow_path, inputs={
        "groundtruth": "3.14",
        "prediction": "3.141592"
    })
    print("\nTest 2 - Close enough:")
    print(f"Score: {result2['score']}")
    
    # Test case 3: Wrong prediction
    result3 = pf.test(flow=flow_path, inputs={
        "groundtruth": "3.14",
        "prediction": "3.15"
    })
    print("\nTest 3 - Wrong answer:")
    print(f"Score: {result3['score']}")
    
    # Test case 4: Error case
    result4 = pf.test(flow=flow_path, inputs={
        "groundtruth": "3.14",
        "prediction": "JSONDecodeError"
    })
    print("\nTest 4 - Error case:")
    print(f"Score: {result4['score']}")

    # Test batch processing
    test_data = [
        {"groundtruth": "1.0", "prediction": "1.0"},
        {"groundtruth": "2.0", "prediction": "2.01"},
        {"groundtruth": "3.14", "prediction": "3.14159"},
        {"groundtruth": "4.0", "prediction": "JSONDecodeError"},
    ]
    
    batch_result = pf.test(
        flow=flow_path,
        inputs=test_data,
    )
    
    print("\nBatch Processing Results:")
    # Print all available keys in batch_result
    print("Available keys:", batch_result.keys() if hasattr(batch_result, 'keys') else "Result is not a dict")
    
    # Try different ways to access metrics
    try:
        if hasattr(batch_result, 'metrics'):
            print(f"Metrics (as attribute): {batch_result.metrics}")
        elif isinstance(batch_result, dict) and 'metrics' in batch_result:
            print(f"Metrics (as dict key): {batch_result['metrics']}")
        elif isinstance(batch_result, dict) and 'output' in batch_result:
            print(f"Output: {batch_result['output']}")
        else:
            print("Raw batch result:", batch_result)
    except Exception as e:
        print(f"Error accessing metrics: {str(e)}")
        print("Raw batch result:", batch_result)

if __name__ == "__main__":
    test_math_evaluation_flow() 