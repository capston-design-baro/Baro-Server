from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.complaint import Complaint
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.ttl_days = 1  # 다운로드 후 1일 뒤 자동 삭제

    def delete_old_complaints(self):
        """다운로드 후 TTL이 지난 고소장 자동 삭제"""
        db: Session = SessionLocal()
        try:
            # 현재 시간 - TTL
            cutoff_time = datetime.now(timezone.utc) - timedelta(days=self.ttl_days)

            # downloaded_at이 cutoff_time보다 이전인 고소장 조회
            old_complaints = db.query(Complaint).filter(
                Complaint.downloaded_at.isnot(None),
                Complaint.downloaded_at < cutoff_time
            ).all()

            if old_complaints:
                deleted_count = len(old_complaints)
                complaint_ids = [c.id for c in old_complaints]

                # 고소장 삭제 (cascade로 chat_messages도 함께 삭제됨)
                for complaint in old_complaints:
                    db.delete(complaint)

                db.commit()
                logger.info(f"Deleted {deleted_count} old complaints (IDs: {complaint_ids}) - TTL: {self.ttl_days} days")
            else:
                logger.info("No old complaints to delete")

        except Exception as e:
            logger.error(f"Error deleting old complaints: {str(e)}")
            db.rollback()
        finally:
            db.close()

    def start(self):
        """스케줄러 시작 - 매일 자정에 실행"""
        # 매일 자정(00:00)에 실행
        self.scheduler.add_job(
            self.delete_old_complaints,
            trigger='cron',
            hour=0,
            minute=0,
            id='delete_old_complaints',
            replace_existing=True
        )

        self.scheduler.start()
        logger.info(f"Scheduler started - Auto-delete complaints after {self.ttl_days} days from download")

    def shutdown(self):
        """스케줄러 종료"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler shutdown")

# 싱글톤 인스턴스
scheduler_service = SchedulerService()
