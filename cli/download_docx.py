import boto3
import io
from docx import Document

def download_and_read_docx(bucket_name, object_key):
    """
    Read a .docx file directly from S3 and return its content as a string
    
    Args:
        bucket_name (str): Name of the S3 bucket
        object_key (str): Path to the object in the bucket
        
    Returns:
        str: Content of the .docx file
    """
    try:
        # Initialize S3 client
        s3_client = boto3.client('s3')
        
        # Get the object directly from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        
        # Read the content stream directly into a BytesIO object
        docx_file = io.BytesIO(response['Body'].read())

        # Open the document from the BytesIO object
        doc = Document(docx_file)
        
        # Extract text from paragraphs
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():  # Only add non-empty paragraphs
                full_text.append(para.text)
        
        # Join all paragraphs with newlines
        return '\n'.join(full_text)
        
    except boto3.exceptions.BotoResponseError as e:
        raise Exception(f"Failed to read from S3: {e}")
    except Exception as e:
        raise Exception(f"Error processing the document: {e}")
