#!/bin/bash
echo "Updating package list..."
apt-get update
echo "Installing Tesseract..."
apt-get install -y tesseract-ocr
echo "Tesseract installation completed."