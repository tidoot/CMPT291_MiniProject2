/**
 * Autogenerated by Thrift Compiler (0.11.0)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
package com.sleepycat.thrift;


public enum TLockDetectMode implements org.apache.thrift.TEnum {
  EXPIRE(1),
  MAX_LOCKS(2),
  MAX_WRITE(3),
  MIN_LOCKS(4),
  MIN_WRITE(5),
  OLDEST(6),
  RANDOM(7),
  YOUNGEST(8);

  private final int value;

  private TLockDetectMode(int value) {
    this.value = value;
  }

  /**
   * Get the integer value of this enum value, as defined in the Thrift IDL.
   */
  public int getValue() {
    return value;
  }

  /**
   * Find a the enum type by its integer value, as defined in the Thrift IDL.
   * @return null if the value is not found.
   */
  public static TLockDetectMode findByValue(int value) { 
    switch (value) {
      case 1:
        return EXPIRE;
      case 2:
        return MAX_LOCKS;
      case 3:
        return MAX_WRITE;
      case 4:
        return MIN_LOCKS;
      case 5:
        return MIN_WRITE;
      case 6:
        return OLDEST;
      case 7:
        return RANDOM;
      case 8:
        return YOUNGEST;
      default:
        return null;
    }
  }
}
