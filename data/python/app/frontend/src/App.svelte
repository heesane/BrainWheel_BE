<!-- App.svelte -->

<script>
  let projectName = "Brain Wheel User Guide";
  let projectDescription = "한국공학대학교 졸업 작품";
  let temp = "http://127.0.0.1:8000/api/task/download";
  let downloadPython = "http://www.codinghhs.tech/api/task/download";
  let api = "http://127.0.0.1:8000/docs";
</script>

<div class="container">
  <h1 class="project-name">{projectName}</h1>
  <p class="project-description">{projectDescription}</p>
</div>
<div class="content-head">
  <div>
    <h1>프로젝트 소개</h1>
    <p>뇌파와 눈으로 컨트롤하는 전동 휠체어</p>
  </div>
</div>
<div class="content-head">
  <div>
    <h1>사용 순서</h1>
    <ol>
      <li>
        <a href={temp}>Python 파일</a>을 다운로드합니다.
      </li>
      <li>다운받은 Python File을 실행시킵니다.</li>
      <li>실행되는 스크립트에서 요구하는 정보를 제공합니다.</li>
      <li>뇌파 센서를 착용하고, 지시되는 동작에 따라 정보를 제공합니다.</li>
      <li>제공받은 데이터를 기반으로 방향에 대한 학습을 진행합니다.</li>
      <li>
        학습이 완료되면, h5파일을 기반으로 새로운 데이터에 대한 검증을
        진행합니다.
      </li>
      <li>검증이 완료되면 전동 휠체어를 사용합니다.</li>
    </ol>
  </div>
</div>
<div class="content-head">
  <div>
    <h1>링크</h1>
    <p>API : <a href={api}>링크</a></p>
  </div>
</div>

<style>
  .container {
    width: fit-content;
    margin: 0 auto;
    padding: 20px;
    border: 3px solid;
    text-align: center;
  }
  .project-name {
    font-size: 50px;
    color: #333;
    margin-bottom: 0;
  }
  .project-description {
    font-size: 33px;
    color: #666;
  }
  .content-head {
    display: flex;
    align-items: center;
    margin-top: 20px;
  }
  .content-head h1 {
    font-size: 24px;
    margin-right: 10px;
  }
  .content-head p {
    font-size: 18px;
    color: #666;
  }
  ol {
    margin-top: 0;
    padding-left: 20px;
  }
</style>
