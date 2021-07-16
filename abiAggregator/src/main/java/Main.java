import com.alibaba.fastjson.JSONException;
import com.alibaba.fastjson.JSONObject;

import java.io.File;
import java.util.concurrent.CountDownLatch;

public class Main {
    public final static String FROM_FOLDER = "./ethereum";
    public final static String TO_FOLDER = "./ethereum_abi_aggregation";
    private final static Object LOCK = new Object();

    public static void main(String[] args) {
        new File(TO_FOLDER).mkdirs();
        createMergeFileNewThread(FROM_FOLDER, TO_FOLDER);
        queryContentByAddress("0xa6461da44a4016d1a3f11fdec5ebbf7fb3ca59b2", TO_FOLDER);
    }

    public static void createMergeFileNewThread(String fromFolder, String toFoler) {
        JSONObject indexJsonObject = new JSONObject();
        File folder = new File(fromFolder);
        File[] files = folder.listFiles();
        if (files == null) {
            System.out.println("files is Empty!");
            return;
        }
        int size = files.length;
        int fileNumber = 30;
        int filees = size / 30 + 1;
        CountDownLatch countDownLatch = new CountDownLatch(fileNumber);
        for (int i = 0; i < fileNumber; i++) {
            int finalI = i;
            new Thread(() -> {
                JSONObject jsonObject = new JSONObject();
                for (int j = finalI * filees; j < (finalI + 1) * filees; j++) {
                    File abi;
                    try {
                        abi = files[j];
                    } catch (IndexOutOfBoundsException e) {
                        FileUtil.writeToFile(toFoler + File.separator + finalI + ".json", jsonObject.toString());
                        countDownLatch.countDown();
                        return;
                    }
                    if (!abi.isDirectory()) {
                        try {
                            String fileName = abi.getName();
                            String content = FileUtil.readFromFile(fromFolder + File.separator + fileName);
                            String key = fileName.replace(".json", "");
                            jsonObject.put(key, content);
                            synchronized (LOCK) {
                                indexJsonObject.put(key, finalI + ".json");
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }
                FileUtil.writeToFile(toFoler + File.separator + finalI + ".json", jsonObject.toString());
                countDownLatch.countDown();
            }).start();
        }
        try {
            countDownLatch.await();
            FileUtil.writeToFile(toFoler + File.separator + "index.json", indexJsonObject.toString());
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static String queryContentByAddress(String address, String indexFolder) {
        String result = "";
        try {
            String indexString = FileUtil.readFromFile(indexFolder + File.separator + "index.json");
            JSONObject indexJson = JSONObject.parseObject(indexString);
            String filename = indexJson.getString(address);
            String detailString = FileUtil.readFromFile(indexFolder + File.separator + filename);
            JSONObject detailJson = JSONObject.parseObject(detailString);
            String contractString = detailJson.getString(address);
            result = contractString;
        } catch (JSONException e) {
            e.printStackTrace();
        }
        System.out.println("result: " + result);
        return result;
    }
}