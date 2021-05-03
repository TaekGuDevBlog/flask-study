6장 Database
- 데이터를 저장 및 보존하는 시스템
  - 데이터 읽기
  - 새로운 데이터 저장
  - 기존 데이터 업데이트
  
- 종류
  - RDBMS
    - 관계형 데이터 모델에 기초를 둔 데이터베이스 시스템
    - ex) Mysql, PostgreSQL 
  - NoSQL
    - 비관계형 타입의 데이터를 저장할 때 주로 씀
    - 관계를 사전에 정의 할 필요가 없음
    - ex) MongoDB, Redis, Cassandra
    
미니터 API (p.127)
- users table
  - id
  - name
  - email
  - profile
 - tweets table
   - id
   - user_id
   - tweet
   
- 테이블들의 상호 관련성 종류 (p.129)
  - one to one
    - 정확히 일대일 매칭
    - ex) 국가 - 수도
  - one to many
    - 하나와 다수
    - ex) users - tweets 관계  (하나의 사용자 - 여러 트윗)
  - many to many 
    - 다수와 다수
    - ex) 사용자 사이의 팔로우하는 관계 (  한 사용자가 여러명을 팔로우 할 수 있고, 해당 사용자 또한 여러 사용자가 팔로우 할 수 있기 때문)
    
정규화
  - 하나의 테이블에 모든 정보를 다 넣으면 되지않냐? 엄청나게 불필요한 중복 데이터가 발생 -> DISK 낭비 오짐
  - 관계형식없이 테이블을 만들고 데이터을 저장하면 실수가 일어 날 수 있다. 각 테이블에 같은 value가 들어가야하는데 오타 발생

트랜잭션 (p.131)
  - 여러 작업이 하나의 작업처럼 취급하여 모두 성공 or 전체 실패
  - 은행 이체 예시
  - ACID ( atomicity, consistency, lsolation, durability )
     - 원자성/atomicity - 모든 작업은 실행 or 롤백
     - 일관성/consistency - 데이터의 일관성 유지
     - 고립성/isolation - 트랜잭션 수행 시 다른 트랜잭션이 끼어들지 못하게 하는것
     - 지속성/durability - 성공한 트랜잭션은 영구반영

