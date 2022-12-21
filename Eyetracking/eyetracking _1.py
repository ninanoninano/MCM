def abalone_exec(epoch_count=10, mb_size=10, report=1):
    load_abalone_dataset() # 데이터 인풋
    init_model() # 모델 생성
    train_and_test(epoch_count, mb_size, report) # 모델 학습