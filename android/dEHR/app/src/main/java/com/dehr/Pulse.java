package com.dehr;

public class Pulse {

    private String id;
    private String key;
    private int pulse;
    private long timestamp;

    Pulse(String id, String key, int pulse, long timestamp) {
        this.id = id;
        this.key = key;
        this.pulse = pulse;
        this.timestamp = timestamp;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public int getPulse() {
        return pulse;
    }

    public void setPulse(int pulse) {
        this.pulse = pulse;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    @Override
    public String toString() {
        return "Pulse{" +
                "id='" + id + '\'' +
                ", key='" + key + '\'' +
                ", pulse=" + pulse +
                ", timestamp=" + timestamp +
                '}';
    }
}
