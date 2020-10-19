FROM ubuntu
LABEL maintainer="kanata <kanata2003@yahoo.co.jp>"
RUN echo "now building..."
RUN apt update && apt install -y curl nkf
COPY solver.sh /root
RUN chmod 777 /root/solver.sh
ENTRYPOINT ["/root/solver.sh"]

# ビルド手順
# docker build -t [任意のイメージ名] .

# 使い方
# docker run --rm --name [任意のコンテナ名] [ビルド時に命名したイメージ名] [問題サーバのIP]
