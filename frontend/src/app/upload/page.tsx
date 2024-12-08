"use client"

import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

const Upload: React.FC = () => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    acceptedFiles.forEach(file => {
      if (file.type !== 'application/pdf') {
        console.error('Only PDF files are allowed');
        return;
      }

      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No token found in local storage.');
        return;
      }

      const formData = new FormData();
      formData.append('files', file);

      fetch('http://localhost:8000/cv/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
        })
        .catch(error => {
          console.error('Error uploading file:', error);
        });
    });
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: { 'application/pdf': [] },
    multiple: true,
  });

  return (
    <div {...getRootProps()} style={styles.dropzone}>
      <input {...getInputProps()} />
      <p>Drag & drop some PDF files here, or click to select files</p>
    </div>
  );
};

const styles = {
  dropzone: {
    border: '2px dashed #cccccc',
    borderRadius: '5px',
    padding: '20px',
    textAlign: 'center' as 'center',
    cursor: 'pointer',
  },
};

export default Upload;
