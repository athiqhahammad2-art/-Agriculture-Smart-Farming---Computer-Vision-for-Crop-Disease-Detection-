import sqlite3
from datetime import datetime
import json

class DatabaseHandler:
    """Handle database operations for predictions and history"""
    
    def __init__(self, db_path='data/predictions.db'):
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize database tables"""
        import os
        os.makedirs('data', exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                image_path TEXT,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_predictions INTEGER,
                disease_counts TEXT,
                avg_confidence REAL,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_prediction(self, disease, confidence, image_path=None, metadata=None):
        """Store prediction in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO predictions (disease, confidence, image_path, metadata, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (disease, confidence, image_path, json.dumps(metadata), timestamp))
        
        conn.commit()
        conn.close()
        
        return timestamp
    
    def get_predictions(self, limit=10):
        """Retrieve prediction history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, disease, confidence, timestamp FROM predictions
            ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'id': r[0],
            'disease': r[1],
            'confidence': r[2],
            'timestamp': r[3]
        } for r in results]
    
    def get_statistics(self):
        """Get prediction statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total predictions
        cursor.execute('SELECT COUNT(*) FROM predictions')
        total = cursor.fetchone()[0]
        
        # Disease distribution
        cursor.execute('''
            SELECT disease, COUNT(*) FROM predictions
            GROUP BY disease ORDER BY COUNT(*) DESC
        ''')
        disease_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Average confidence
        cursor.execute('SELECT AVG(confidence) FROM predictions')
        avg_confidence = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_predictions': total,
            'disease_distribution': disease_counts,
            'average_confidence': float(avg_confidence),
            'timestamp': datetime.now().isoformat()
        }
    
    def clear_old_predictions(self, days=30):
        """Remove predictions older than specified days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM predictions
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        conn.commit()
        conn.close()