#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

echo "Shell 传递参数实例！";
echo "第一个参数为：$1";

echo "参数个数为：$#";
echo "传递的参数作为一个字符串显示：$*";
your_name="qinjx"
echo $your_name
echo ${your_name}

your_name="tom"
echo $your_name
your_name="alibaba"
echo $your_name
for skill in Ada Coffe Action Java;do
    echo "I am good at ${skill}Script"
done

for file in $(ls ~/桌面);do
  echo ${file}
done


myUrl="http://www.runoob.com"
unset myUrl
echo $myUrl


your_name='runoob'
str="Hello, I know you are \"$your_name\"! \n"
str1="Hello, I know you are \"$your_name\"!gggg \n"
echo -e $str
echo -e $str1


your_name="runoob"
# 使用双引号拼接
greeting="hello, "$your_name" !"
greeting_1="hello, ${your_name} !"
echo $greeting  $greeting_1
# 使用单引号拼接
greeting_2='hello, '$your_name' !'
greeting_3='hello, ${your_name} !'
echo $greeting_2  $greeting_3

my_array=(A B "C" D)

echo "第一个元素为: ${my_array[0]}"
echo "第二个元素为: ${my_array[1]}"
echo "第三个元素为: ${my_array[2]}"
echo "第四个元素为: ${my_array[3]}"


my_array[0]=A
my_array[1]=B
my_array[2]=C
my_array[3]=D

echo "数组的元素为: ${my_array[*]}"
echo "数组的元素为: ${my_array[@]}"


my_array[0]=A
my_array[1]=B
my_array[2]=C
my_array[3]=D

echo "数组元素个数为: ${#my_array[*]}"
echo "数组元素个数为: ${#my_array[@]}"

val=`expr 28 / 9`
echo "两数之和为 : $val"


