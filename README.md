# Persona Fusion

Unified public-figure profiling and cross-platform social signal analysis using Wikipedia, X, YouTube, Instagram, and Facebook data.

## Overview

This project collects and integrates public data for 10 public figures across multiple platforms into a single unified dataset. It combines official APIs where available with practical fallbacks when platform restrictions block direct access.

## Data Sources

* Wikipedia REST API
* X API
* YouTube Data API
* Instagram via undocumented public profile path fallback
* Facebook via Apify scraper

## Features

* Unified profile collection for 10 public figures
* Cross-platform handle mapping
* Normalized output schema
* CSV export for downstream analysis
* Environment-based credential management with `.env`

## Tech Stack

* Python
* pandas
* requests
* Apify
* python-dotenv

## Output

The main output is a unified CSV dataset containing profile metadata and selected public engagement fields across platforms.

## Notes

Some Meta platform data could not be collected through official public APIs due to access restrictions. For this reason, Instagram and Facebook required alternative collection methods.
